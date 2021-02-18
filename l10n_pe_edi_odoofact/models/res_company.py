# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

from datetime import date, datetime, timedelta
from odoo.fields import Date, Datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    l10n_pe_edi_ose_url = fields.Char('URL')
    l10n_pe_edi_ose_token = fields.Char('Token')
    l10n_pe_edi_ose_id = fields.Many2one('l10n_pe_edi.supplier', string='PSE / OSE Supplier')   
    l10n_pe_edi_ose_code = fields.Char('Code of PSE / OSE supplier', related='l10n_pe_edi_ose_id.code')
    l10n_pe_edi_resume_url = fields.Char('Resume URL')
    l10n_pe_edi_multishop = fields.Boolean('Multi-Shop')
    l10n_pe_edi_shop_ids = fields.One2many('l10n_pe_edi.shop','company_id', string='Shops')
