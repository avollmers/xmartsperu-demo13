# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sh_show_amount = fields.Boolean(string='Show Amount',
                                    related='company_id.sh_show_amount',
                                    readonly=False
                                    )
    sh_show_invoice_status_in_pdf = fields.Boolean(
        string='Show Invoice Status In Pdf',
        related='company_id.sh_show_invoice_status_in_pdf',
        readonly=False
        )
    sh_total_amount = fields.Float(string='Total Amount', compute='_compute_all_amount')
    sh_paid_amount = fields.Float(string='Paid Amount', compute='_compute_all_amount')
    sh_balance_amount = fields.Float(string='Balance', compute='_compute_all_amount')
    sh_invoice_status = fields.Selection([('not_paid', 'Invoice not paid'),
                                          ('partially_paid', 'Invoice partially paid'),
                                          ('fully_paid', 'Invoice fully paid')],
                                          compute='_compute_all_amount',
                                          string='Invoice Status',
                                          default='not_paid')
    hide_validate_button = fields.Boolean(string='Hide Validate', compute='_compute_hide_validate')

    def _compute_all_amount(self):
        if self:
            for rec in self:
                rec.sh_total_amount = 0.0
                rec.sh_paid_amount = 0.0
                rec.sh_balance_amount = 0.0
                rec.sh_invoice_status = 'not_paid'
                if rec.sale_id:
                    paid_amount = 0.0
                    total_amount = rec.sale_id.amount_total
                    rec.sh_total_amount = total_amount
                    rec.sh_balance_amount = total_amount - paid_amount
                    if rec.picking_type_code == 'outgoing' and rec.sale_id and rec.sale_id.invoice_ids:
                        for invoice in rec.sale_id.mapped('invoice_ids'):
                            if invoice.state in ['posted']:
                                paid_amount += invoice.amount_total
                        rec.sh_paid_amount = paid_amount
                        rec.sh_balance_amount = total_amount - rec.sh_paid_amount
    
                        if rec.sh_total_amount == rec.sh_paid_amount:
                            rec.sh_invoice_status = 'fully_paid'
                        elif rec.sh_paid_amount < rec.sh_total_amount and rec.sh_paid_amount != 0.0:
                            rec.sh_invoice_status = 'partially_paid'
                        elif rec.sh_paid_amount < rec.sh_total_amount and rec.sh_paid_amount == 0.0:
                            rec.sh_invoice_status = 'not_paid'
                    else:
                        rec.sh_paid_amount = 0.0
                        rec.sh_balance_amount = 0.0

    def _compute_hide_validate(self):
        if self:
            for rec in self:
                rec.hide_validate_button = False
                if rec.sale_id:
                    if rec.company_id.sh_restrict_validate == 'none':
                        rec.hide_validate_button = True
                    elif rec.company_id.sh_restrict_validate == 'partial_payment' and rec.sh_invoice_status == 'partially_paid':
                        rec.hide_validate_button = True
                    elif rec.company_id.sh_restrict_validate == 'full_payment' and rec.sh_invoice_status == 'fully_paid':
                        rec.hide_validate_button = True
                    else:
                        rec.hide_validate_button = False
