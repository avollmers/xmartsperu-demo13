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

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_pe_edi_multishop = fields.Boolean('Multi-Shop', related='company_id.l10n_pe_edi_multishop', readonly=False)
    l10n_pe_edi_ose_id = fields.Many2one('l10n_pe_edi.supplier', string='PSE / OSE', related='company_id.l10n_pe_edi_ose_id', readonly=False)
    l10n_pe_edi_ose_code = fields.Char('Code of supplier', related='l10n_pe_edi_ose_id.code')
    l10n_pe_edi_ose_url = fields.Char('URL', related='company_id.l10n_pe_edi_ose_url', readonly=False)
    l10n_pe_edi_ose_token = fields.Char('Token', related='company_id.l10n_pe_edi_ose_token', readonly=False)

