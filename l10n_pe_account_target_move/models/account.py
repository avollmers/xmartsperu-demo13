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

import time
import math
import re

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools
from odoo.tests.common import Form


class AccountAccount(models.Model):
    _inherit = "account.account"
    
    debit_target_account_id = fields.Many2one('account.account', string='Debit target account')
    credit_target_account_id = fields.Many2one('account.account', string='Credit target account')
    target_journal_id = fields.Many2one('account.journal', string='Target journal')
    target_account = fields.Boolean(string='Has target account', default=False)
    
