# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY Odoo Peru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import json, requests, pytz

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    l10n_pe_edi_is_epicking = fields.Boolean(string="Is E-picking", default=False, copy=False)
    l10n_pe_edi_picking_sequence_id = fields.Many2one('ir.sequence', string="E-Picking Sequence", copy=False)
    l10n_pe_edi_shop_id = fields.Many2one('l10n_pe_edi.shop', string='Shop')

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'date desc'

    #---------SEND OSE-------------------

    l10n_pe_edi_picking_company_partner_id = fields.Many2one('res.partner', string="Company Partner", related='company_id.partner_id')
    l10n_pe_edi_picking_partner_id = fields.Many2one('res.partner', string="Partner", related='partner_id.commercial_partner_id')
    l10n_pe_edi_picking_name = fields.Char(string="E-Picking Name", readonly=True, copy=False)
    l10n_pe_edi_picking_serie = fields.Char(string="Serie", store=True, readonly=True, copy=False)
    l10n_pe_edi_picking_number = fields.Integer(string="Number", store=True, readonly=True, copy=False)
    l10n_pe_edi_picking_observations = fields.Char(string='Observations', size=1000, help="If you want line breaks for the printed or PDF representation use <br>", copy=False)
    l10n_pe_edi_picking_catalog_20_id = fields.Many2one('l10n_pe_edi.catalog.20', string="Reason for transfer")
    l10n_pe_edi_picking_total_gross_weight = fields.Float(string="Total Gross Weight", default=0.0, help='Weight in Kg.')
    l10n_pe_edi_picking_number_packages = fields.Integer(string="Number Of Packages", default=0)
    l10n_pe_edi_picking_catalog_18_id = fields.Many2one('l10n_pe_edi.catalog.18', string="Transport Type")
    l10n_pe_edi_picking_start_transport_date = fields.Date(string="Start Transport Date", copy=False)
    l10n_pe_edi_picking_carrier_id = fields.Many2one('res.partner', string="Carrier")
    l10n_pe_edi_picking_carrier_license_plate = fields.Char(string="License Plate")
    l10n_pe_edi_picking_driver_id = fields.Many2one('res.partner', string="Driver")
    l10n_pe_edi_multishop = fields.Boolean('Multi-Shop', related='company_id.l10n_pe_edi_multishop')     
    l10n_pe_edi_shop_id = fields.Many2one('l10n_pe_edi.shop', string='Shop', related='picking_type_id.l10n_pe_edi_shop_id', store=True)
    l10n_pe_edi_picking_starting_point_id = fields.Many2one('res.partner', string="Starting Point")
    l10n_pe_edi_picking_arrival_point_id = fields.Many2one('res.partner', string="Arrival Point")
    l10n_pe_edi_is_epicking = fields.Boolean(string="Is E-picking", readonly=True, copy=False)
    l10n_pe_edi_ose_accepted = fields.Boolean('Sent to PSE/OSE', related='l10n_pe_edi_request_id.ose_accepted', store=True)
    l10n_pe_edi_request_id = fields.Many2one('l10n_pe_edi.request', string='PSE/OSE request', copy=False)
    l10n_pe_edi_response = fields.Text('Response', related='l10n_pe_edi_request_id.response', store=True)
    l10n_pe_edi_sunat_accepted = fields.Boolean('Accepted by SUNAT', related='l10n_pe_edi_request_id.sunat_accepted', store=True)
    
    #-----------COMPUTE & ONCHANGE----------------
    
    def _compute_serie_number(self):
        for rec in self:
            if rec.l10n_pe_edi_picking_name:
                name = rec.l10n_pe_edi_picking_name.split('-')
                if len(name) == 2:
                    rec.l10n_pe_edi_picking_serie = name[0]
                    rec.l10n_pe_edi_picking_number = int(name[1])

    #-----------METHODS---------------------------

    def convert_date_to_timezone(self, date_time):
        if self.env.user.tz:
            tz = pytz.timezone(self.env.user.tz)
            return pytz.utc.localize(date_time).astimezone(tz)
        else:
            return date_time

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('e_picking_name', False):
                # Only goes off when the custom_search is in the context values.
                result.append((record.id, "{}".format(record.l10n_pe_edi_picking_name)))
            else:
                result.append((record.id, record.name))
        return result

    def convert_to_epicking(self):
        if self.state != 'done':
            raise UserError(_("This document cannot be converted to electronic picking. The picking should be done"))
        if self.picking_type_id.l10n_pe_edi_is_epicking:
            if self.l10n_pe_edi_picking_partner_id.l10n_latam_identification_type_id and self.l10n_pe_edi_picking_partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code == '6' and self.l10n_pe_edi_picking_partner_id.vat:
                self.l10n_pe_edi_is_epicking = True
                if not self.l10n_pe_edi_picking_name:
                    self.l10n_pe_edi_picking_name = self.picking_type_id.l10n_pe_edi_picking_sequence_id.next_by_id()
            else:
                raise UserError(_("This document cannot be converted to electronic picking. The partner doesn't have RUC"))
        else:
            raise UserError(_("You cannot convert this document to electronic picking. Configure the settings of 'Picking operation type'"))
        self._compute_serie_number()

    def _get_picking_lines_values_odoofact(self, lines):
        data = []
        for item in lines:
            values = {
                'unidad_de_medida': item.product_id.type == 'service' and 'ZZ' or 'NIU',
                'codigo': item.product_id.default_code or '',
                'descripcion': item.product_id.name,
                'cantidad': item.qty_done,
            }
            data.append(values)
        return data
    
    @api.model
    def _get_partner_address(self, partner):
        res = ''
        if partner:
            if partner.street:
                res += partner.street
            if partner.street_number:
                res += ' ' + partner.street_number
            if partner.street_number2:
                res += ', ' + partner.street_number2
            if partner.l10n_pe_district:
                res += ', ' + partner.l10n_pe_district.name
            if partner.city_id:
                res += ', ' + partner.city_id.name
            if partner.state_id:
                res += ', ' + partner.state_id.name
        return res

    def _get_picking_values_odoofact(self):
        values = {
            'company_id': self.company_id.id,
            'l10n_pe_edi_shop_id': self.l10n_pe_edi_shop_id and self.l10n_pe_edi_shop_id.id or False,
            'picking_id': self.id,
            'operacion': "generar_guia",
            'tipo_de_comprobante': 7,
            'serie': str(self.l10n_pe_edi_picking_serie),
            'numero': self.l10n_pe_edi_picking_number,
            'cliente_tipo_de_documento': str(self.l10n_pe_edi_picking_partner_id.l10n_latam_identification_type_id and self.l10n_pe_edi_picking_partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code) if self.l10n_pe_edi_picking_partner_id.l10n_latam_identification_type_id else '1',
            'cliente_numero_de_documento': self.l10n_pe_edi_picking_partner_id.vat,      
            'cliente_denominacion': self.l10n_pe_edi_picking_partner_id.name,
            'cliente_direccion': self._get_partner_address(self.partner_id),
            'observaciones': self.note,
            'fecha_de_emision': self.date_done and self.convert_date_to_timezone(self.date_done).strftime("%d-%m-%Y") or '',
            'motivo_de_traslado': self.l10n_pe_edi_picking_catalog_20_id and self.l10n_pe_edi_picking_catalog_20_id.code or '',
            'peso_bruto_total': self.l10n_pe_edi_picking_total_gross_weight or 0.0,
            'numero_de_bultos': self.l10n_pe_edi_picking_number_packages or 0,
            'tipo_de_transporte': self.l10n_pe_edi_picking_catalog_18_id and self.l10n_pe_edi_picking_catalog_18_id.code or '',
            'fecha_de_inicio_de_traslado': self.l10n_pe_edi_picking_start_transport_date and self.l10n_pe_edi_picking_start_transport_date.strftime('%d-%m-%Y') or '',
            'transportista_documento_tipo': self.l10n_pe_edi_picking_carrier_id and (self.l10n_pe_edi_picking_carrier_id.l10n_latam_identification_type_id and self.l10n_pe_edi_picking_carrier_id.l10n_latam_identification_type_id.l10n_pe_vat_code or '') or '',
            'transportista_documento_numero': self.l10n_pe_edi_picking_carrier_id.vat or '',
            'transportista_denominacion': self.l10n_pe_edi_picking_carrier_id.name,
            'transportista_placa_numero': self.l10n_pe_edi_picking_carrier_license_plate,
            'conductor_documento_tipo': self.l10n_pe_edi_picking_driver_id.l10n_latam_identification_type_id and self.l10n_pe_edi_picking_driver_id.l10n_latam_identification_type_id.l10n_pe_vat_code or '',
            'conductor_documento_numero': self.l10n_pe_edi_picking_driver_id.vat or '',
            'conductor_denominacion': self.l10n_pe_edi_picking_driver_id.name,
            'punto_de_partida_ubigeo': self.l10n_pe_edi_picking_starting_point_id.l10n_pe_district and self.l10n_pe_edi_picking_starting_point_id.l10n_pe_district.code or self.l10n_pe_edi_picking_starting_point_id.zip,
            'punto_de_partida_direccion': self._get_partner_address(self.l10n_pe_edi_picking_starting_point_id),
            'punto_de_llegada_ubigeo': self.l10n_pe_edi_picking_arrival_point_id.l10n_pe_district and self.l10n_pe_edi_picking_arrival_point_id.l10n_pe_district.code or self.l10n_pe_edi_picking_arrival_point_id.zip,
            'punto_de_llegada_direccion': self._get_partner_address(self.l10n_pe_edi_picking_arrival_point_id),
            'enviar_automaticamente_a_la_sunat': "false",
            'enviar_automaticamente_al_cliente': "false",
            'codigo_unico': '%s|%s|%s-%s' %('odoo',self.company_id.partner_id.vat,self.l10n_pe_edi_picking_serie,str(self.l10n_pe_edi_picking_number)),
            'items': self._get_picking_lines_values_odoofact(self.move_line_ids_without_package),
        }
        return values

    def _get_picking_values_check_odoofact(self):
        """
        Prepare the dict of values to create the request for checking the document status. Valid for Nubefact.
        """
        self.ensure_one()
        values = {    
            'company_id': self.company_id.id,
            'operacion': 'consultar_guia',
            'tipo_de_comprobante': 7,
            'serie': self.l10n_pe_edi_picking_serie,
            'numero': str(self.l10n_pe_edi_picking_number)
        }
        return values

    def _get_ose_supplier(self):
        if not self.company_id.l10n_pe_edi_ose_id:
            raise UserError(_('Please select a PSE/OSE supplier for the company %s')%(self.company_id.name,))
        return self.company_id.l10n_pe_edi_ose_id.code

    def action_document_send(self):
        if not self.l10n_pe_edi_is_epicking:
            raise UserError(_("The Picking is not a Electronic Document"))
        if not self.l10n_pe_edi_picking_carrier_id.l10n_latam_identification_type_id and not self.l10n_pe_edi_picking_carrier_id.vat:
            raise UserError(_("Carrier doesn't have document number or document type assigned"))
        if not self.l10n_pe_edi_picking_driver_id.l10n_latam_identification_type_id and not self.l10n_pe_edi_picking_driver_id.vat:
            raise UserError(_("Driver doesn't  have document number or document type assigned"))
        for picking in self:
            if picking.state == 'draft':
                continue
            if picking.company_id.l10n_pe_edi_multishop and not picking.l10n_pe_edi_shop_id:
                raise UserError(_("Review the Journal configuration and select a shop: \n Journal: %s")% (move.journal_id.name))
            ose_supplier = picking._get_ose_supplier()
            vals = getattr(picking,'_get_picking_values_%s' % ose_supplier)()
            if not picking.l10n_pe_edi_request_id:
                l10n_pe_edi_request_id = self.env['l10n_pe_edi.request'].create({
                    'company_id': picking.company_id.id,
                    'document_number': picking.l10n_pe_edi_picking_name,
                    'l10n_pe_edi_shop_id': picking.l10n_pe_edi_shop_id and picking.l10n_pe_edi_shop_id.id or False,
                    'model': self._name, 
                    'res_id': self.id, 
                    'type': 'picking', 
                    'document_date': picking.date_done})
                picking.write({'l10n_pe_edi_request_id': l10n_pe_edi_request_id})
            else:
                l10n_pe_edi_request_id = picking.l10n_pe_edi_request_id
            if not picking.l10n_pe_edi_ose_accepted:
                l10n_pe_edi_request_id.action_api_connect(vals)
            else:
                picking.action_document_check()
    
    def action_document_check(self):
        """
        Send the request for Checking document status for electronic pickings
        """
        for picking in self:
            ose_supplier = picking._get_ose_supplier()
            vals = getattr(picking,'_get_picking_values_check_%s' % ose_supplier)()
            if picking.l10n_pe_edi_request_id:
                picking.l10n_pe_edi_request_id.action_api_connect(vals)

    @api.model
    def cron_send_pickings(self):
        picking_ids = self.env['stock.picking'].search([
            ('l10n_pe_edi_is_epicking','=',True),
            ('state','not in',['draft','cancel']),
            ('l10n_pe_edi_ose_accepted','=',False)]).filtered(lambda inv: inv.scheduled_date != False)
        for picking in picking_ids:
            picking.action_document_send()
    
    @api.model
    def cron_check_pickings(self):
        picking_ids = self.env['stock.picking'].search([
            ('l10n_pe_edi_is_epicking','=',True),
            ('state','not in',['draft','cancel']),
            ('l10n_pe_edi_ose_accepted','=',True),
            ('l10n_pe_edi_sunat_accepted','=',False)]).filtered(lambda inv: inv.scheduled_date != False)
        for picking in picking_ids:
            picking.action_document_check()
    
    def action_open_edi_request(self):
        """ 
        This method opens the EDI request 
        """
        self.ensure_one()
        if self.l10n_pe_edi_request_id:
            return {
                'name': _('EDI Request'),
                'view_mode': 'form',
                'res_model': 'l10n_pe_edi.request',
                'res_id': self.l10n_pe_edi_request_id.id,
                'type': 'ir.actions.act_window',
            }
        return True
