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
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class AccountMove(models.Model):
    _inherit = "account.move"
    
    origin_move_id = fields.Many2one('account.move', string='Origin entry', copy=False)
    origin_move_line_id = fields.Many2one('account.move.line', string='Origin move line', copy=False)
    target_move_ids = fields.One2many('account.move', 'origin_move_id', string='Target entries', copy=False)
    target_move_count = fields.Integer('Target move count', compute='_compute_count_target_move')

    def _compute_count_target_move(self):
        account_move = self.env['account.move']
        for record in self:
            record.target_move_count = account_move.search_count([('origin_move_id', '=', record.id)])

    def post(self):
        super(AccountMove, self).post()        
        for move in self:
            for l in move.line_ids.filtered(lambda r: r.account_id.target_account == True):
                # account_id = l.account_id.id
                if not l.target_move_id:
                    move_data = {
                                'origin_move_id': move.id,
                                'origin_move_line_id': l.id,
                                'ref': l.name,
                                'date': l.date,
                                'journal_id': l.account_id.target_journal_id and l.account_id.target_journal_id.id or False,
                                'type': 'entry',
                                }
                    target_move_id = self.env['account.move'].create(move_data)
                    l.target_move_id = target_move_id

                line_data = {
                            'origin_move_id': move.id,
                            'origin_move_line_id': l.id,
                            'name': l.name,
                            'ref': move.name,
                            'partner_id': l.partner_id and l.partner_id.id or False,                                    
                            'currency_id': l.currency_id and l.currency_id.id or False,
                        }
                debit_data = dict(line_data)
                credit_data = dict(line_data)

                if l.debit != False:
                    debit_data.update(
                            account_id = l.account_id.debit_target_account_id.id,
                            debit = l.debit,
                            credit = False,
                            amount_currency = l.amount_currency,
                        )
                    credit_data.update(
                            account_id = l.account_id.credit_target_account_id.id,
                            debit = False,
                            credit = l.debit,
                            amount_currency = l.amount_currency * -1.0,
                    )
                else:
                    debit_data.update(                                   
                            account_id = l.account_id.debit_target_account_id.id,
                            debit = False,
                            credit = l.credit,
                            amount_currency = l.amount_currency,
                    )
                    credit_data.update(
                            account_id = l.account_id.credit_target_account_id.id,
                            debit = l.credit,
                            credit = False,
                            amount_currency = l.amount_currency * -1.0,
                    )
                
                if not l.target_move_id.line_ids:
                    l.target_move_id.write({
                        'line_ids': [(0, 0, debit_data), (0, 0, credit_data)]
                    })
                else:
                    for line in l.target_move_id.line_ids:
                        if line.account_id.id == l.account_id.debit_target_account_id.id:
                            line.write(debit_data)
                        if line.account_id.id == l.account_id.credit_target_account_id.id:
                            line.write(credit_data)
                # Post Target move
                if l.target_move_id.state == 'draft':
                    l.target_move_id.post()

        return True
    
    def button_draft(self):
        super(AccountMove, self).button_draft()  
        for move in self:
            for target in move.target_move_ids:
                target.button_draft()

    def button_cancel(self):
        super(AccountMove, self).button_cancel()  
        for move in self:
            for target in move.target_move_ids:
                target.button_cancel()
    
    def open_target_move_view(self):
        [action] = self.env.ref('account.action_move_line_form').read()
        ids = self.target_move_ids.ids
        action['domain'] = [('id', 'in', ids)]
        action['name'] = 'Target entries'
        return action

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    origin_move_id = fields.Many2one('account.move', string='Origin entry', copy=False)
    origin_move_line_id = fields.Many2one('account.move.line', string='Origin move line', ondelete='cascade')
    target_move_id = fields.Many2one('account.move', string='Target entry', copy=False)