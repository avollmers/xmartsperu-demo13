# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import tempfile
import binascii
import xlrd
import io
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime
from odoo.exceptions import Warning
from odoo import models, fields, api, _
import csv
import base64


class SrImportPurchase(models.TransientModel):
    _name = "sr.import.purchase"

    select_file = fields.Binary('File')
    sequence_option = fields.Selection([('custom', 'Use Excel/CSV Sequence Number'), ('system', 'Use System Default Sequence Number')], string='Sequence Option', default='custom')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    stage_option = fields.Selection(
        [('draft', 'Import Draft Purchase'), ('confirm', 'Confirm Purchase Automatically With Import')],
        string="Purchase Stage Option", default='draft')
    import_product_option = fields.Selection([('name', 'Name'), ('code', 'Code'), ('barcode', 'Barcode')], string='Import Product By ', default='name')
    import_vendor_option = fields.Selection([('name', 'Name'), ('code', 'Internal Reference')], string='Import Vendor By ', default='name')        

    def import_purchase(self):
        try:
            if self.import_option == 'xls':
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.select_file))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
                for row_no in range(sheet.nrows):
                    val = {}
                    if row_no <= 0:
                        fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
                    else:
                        line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                        date_tuple = xlrd.xldate_as_tuple(float(line[5]), workbook.datemode)
                        date = datetime(*date_tuple).strftime('%Y-%m-%d')
                        values.update({'number':line[0],
                                        'vendor': line[1],
                                        'vendor_reference': line[2],
                                        'currency': line[3],
                                        'company': line[4],
                                        'date': date,
                                        'product': line[6],
                                        'description': line[7],
                                        'quantity': line[8],
                                        'uom': line[9],
                                        'price': line[10],
                                        'tax': line[11],
                                        })
                        res = self.create_purchase(values)
            else:
                keys = ['number', 'vendor', 'vendor_reference', 'currency', 'company', 'date', 'product', 'description', 'quantity', 'uom', 'price', 'tax']
                try:
                    csv_data = base64.b64decode(self.select_file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    data_file.seek(0)
                    file_reader = []
                    values = {}
                    csv_reader = csv.reader(data_file, delimiter=',')
                    file_reader.extend(csv_reader)
                except:
                    raise Warning(_("Invalid file!"))
                for i in range(len(file_reader)):
                    field = list(map(str, file_reader[i]))
                    values = dict(zip(keys, field))
                    if values:
                        if i == 0:
                            continue
                        else:
                            res = self.create_purchase(values)
        except Exception as e:
            raise Warning(_(e))

    def _find_vendor(self, vendor):
        if self.import_vendor_option == 'name':
            vendor_id = self.env['res.partner'].search([('name', '=', vendor)])
        else:
            vendor_id = self.env['res.partner'].search([('ref', '=', vendor)])
        if vendor_id:
            return vendor_id
        else:
            raise Warning(_('"%s" Vendor not in your system') % vendor)

    def _find_currency(self, currency):
        currency_id = self.env['res.currency'].search([('name', '=', currency)])
        if currency_id:
            return currency_id
        else:
            raise Warning(_('"%s" Currency not in your system') % currency)

    def _find_compnay(self, company):
        company_id = self.env['res.company'].search([('name', '=', company)])
        if company_id:
            return company_id
        else:
            raise Warning(_('"%s" Company not in your system') % company)

    def create_purchase(self, values):
        vendor = self._find_vendor(values.get('vendor'))
        currency = self._find_currency(values.get('currency'))
        company = self._find_compnay(values.get('company'))
        purchase_id = self.env['purchase.order'].search([('name', '=', values.get('number'))])
        if purchase_id:
            if purchase_id.partner_id.id == vendor.id:
                if purchase_id.currency_id.id == currency.id:
                    if purchase_id.company_id.id == company.id:
                        self.create_purchase_order_line(purchase_id, values)
                    else:
                        raise Warning(_('Company is different for %s, \n Please define same' % values.get('number')))
                else:
                    raise Warning(_('Currency is different for %s, \n Please define same' % values.get('number')))
            else:
                raise Warning(_('Vendor is different for %s, \n Please define same' % values.get('number')))
        else:
            purchase = self.env['purchase.order'].create({
                    'name':self.env['ir.sequence'].next_by_code('purchase.order') if self.sequence_option == 'system' else values.get('number'),
                    'partner_id':vendor.id,
                    'partner_ref': values.get('vendor_reference'),
                    'currency_id': currency.id,
                    'date_order': values.get('date'),
                    'company_id':company.id,
                    'state':'draft',
                    'date_planned':datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                })
            self.create_purchase_order_line(purchase, values)
            if self.stage_option == 'confirm':
                purchase.button_confirm()
            

    def _find_product(self, product):
        if self.import_product_option == 'name':
            product_id = self.env['product.product'].search([('name', '=', product)])
        elif self.import_product_option == 'code':
            product_id = self.env['product.product'].search([('default_code', '=', product)])
        else:
            product_id = self.env['product.product'].search([('barcode', '=', product)])
        if product_id:
            return product_id
        else:
            raise Warning(_('"%s" Product not in your system') % product)

    def _find_uom(self, uom):
        uom_id = self.env['uom.uom'].search([('name', '=', uom)])
        if uom_id:
            return uom_id
        else:
            raise Warning(_('"%s" Unit Of Measure not in your system') % uom)

    def create_purchase_order_line(self, purchase_id, values):
        product = self._find_product(values.get('product'))
        uom = self._find_uom(values.get('uom'))
        tax_ids = []
        if values.get('tax'):
            tax_names = values.get('tax').split(',')
            for name in tax_names:
                tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', 'purchase')])
                if not tax:
                    raise Warning(_('"%s" Tax not in your system') % name)
                tax_ids.append(tax.id)
        self.env['purchase.order.line'].create(
            {
                'product_id':product.id,
                'name': values.get('description'),
                'product_qty': values.get('quantity'),
                'product_uom': uom.id,
                'price_unit':values.get('price'),
                'taxes_id':([(6, 0, tax_ids)]),
                'order_id': purchase_id.id,
                'date_planned':datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                })
        return True

