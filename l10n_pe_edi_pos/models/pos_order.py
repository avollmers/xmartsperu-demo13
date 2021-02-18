# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging
from odoo.exceptions import UserError,Warning

_logger = logging.getLogger(__name__)


class pos_order(models.Model):
    _inherit = "pos.order"

    invoice_journal_id = fields.Many2one('account.journal', 'Journal account', readonly=1)
    
    def _prepare_invoice_vals(self):
        values = super(pos_order, self)._prepare_invoice_vals()
        if self.invoice_journal_id:
            values['journal_id'] = self.invoice_journal_id.id
        
        return values

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)
        if ui_order.get('invoice_journal_id', False):
            order_fields['invoice_journal_id'] = ui_order.get('invoice_journal_id')
        
        return order_fields