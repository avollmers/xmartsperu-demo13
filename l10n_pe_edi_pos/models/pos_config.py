# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class pos_config(models.Model):
    _inherit = "pos.config"

    def _default_invoice_journal_ids(self):
        return self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.env.company.id)], limit=1)

    # module_einvoice = fields.Boolean(string='Electronic Invoicing', help='Enables electronic invoice generation from the Point of Sale.')
    invoice_journal_ids = fields.Many2many(
        'account.journal',
        'pos_config_invoice_journal_rel',
        'config_id',
        'journal_id',
        'Accounting Invoice Journal',
        help="Invoice journals for Electronic invoices.",
        default=_default_invoice_journal_ids)
    default_partner_id = fields.Many2one("res.partner", string="Client by default", help="This client will be set by default in the order")
    
    # @api.onchange('module_einvoice')
    # def _onchange_module_einvoice(self):
    #     if self.module_einvoice:
    #         self.module_account = False
    
    
    
    