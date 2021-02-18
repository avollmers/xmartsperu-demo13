# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    base_uuid = fields.Text(string="DB:",default= lambda self : self.env["ir.config_parameter"].search([("key","=","database.uuid")]).value)
    active = fields.Boolean ("Tasa de cambio automatica")
    group_multi_currency = fields.Boolean(related = "active_multi_currency", readonly = False)
    active_multi_currency = fields.Boolean(default = True)
    
    currency_interval_unit = fields.Selection(related="company_id.currency_interval_unit", readonly=False)
    currency_provider = fields.Selection(related="company_id.currency_provider", readonly=False)
    currency_next_execution_date = fields.Date(related="company_id.currency_next_execution_date", readonly=False)

    @api.onchange('currency_interval_unit')
    def onchange_currency_interval_unit(self):
        if self.currency_interval_unit == 'daily':
            next_update = relativedelta(days=+1)
        elif self.currency_interval_unit == 'weekly':
            next_update = relativedelta(weeks=+1)
        elif self.currency_interval_unit == 'monthly':
            next_update = relativedelta(months=+1)
        else:
            self.currency_next_execution_date = False
            return
        self.currency_next_execution_date = datetime.date.today() + next_update

    def update_currency_rates_manually(self):
        self.ensure_one()

        if not (self.company_id.update_currency_rates()):
            raise UserError(_('Unable to connect to the online exchange rate platform. The web service may be temporary down. Please try again in a moment.'))

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    currency_provider = fields.Selection([
        ('ecb', 'European Central Bank'),
        ('fta', 'Federal Tax Administration (Switzerland)'),
        ('banxico', 'Mexican Bank'),
        ('boc', 'Bank Of Canada'),
        ('xe_com', 'xe.com'),
        ("xmarts_peru","Xmarts Perú")
    ], default='xmarts_peru', string='Service Provider')
    currency_interval_unit = fields.Selection([
        ('manually', 'Manually'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')],
        default='daily', string='Interval Unit')
    currency_next_execution_date = fields.Date(string="Next Execution Date")

