# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create_from_ui(self, partner):
        partner.update({'l10n_latam_identification_type_id': int(partner.get('l10n_latam_identification_type_id', ''))})
        res = super(ResPartner, self).create_from_ui(partner)
        return res
            