# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompnay(models.Model):
    _inherit = 'res.company'

    sh_show_amount = fields.Boolean(string='Show Amount')
    sh_show_invoice_status_in_pdf = fields.Boolean(
        string='Show Invoice Status In Pdf'
        )
    sh_restrict_validate = fields.Selection([('none', 'None'),
                                             ('partial_payment', 'Partial Payment'),
                                             ('full_payment', 'Full Payment')],
                                            default='none',
                                            string='Restict/Hide Validate Button in Picking')

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_show_amount = fields.Boolean(string='Show Amount',
                                    related='company_id.sh_show_amount',
                                    readonly=False
                                    )
    sh_show_invoice_status_in_pdf = fields.Boolean(
        string='Show Invoice Status In Pdf',
        related='company_id.sh_show_invoice_status_in_pdf',
        readonly=False
        )
    sh_restrict_validate = fields.Selection([('none', 'None'),
                                             ('partial_payment', 'Partial Payment'),
                                             ('full_payment', 'Full Payment')],
                                            default='none',
                                            string='Restict/Hide Validate Button in Picking',
                                            related='company_id.sh_restrict_validate',
                                            readonly=False)
