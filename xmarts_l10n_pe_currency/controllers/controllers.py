# -*- coding: utf-8 -*-
# from odoo import http


# class XmartsL10nPeCurrency(http.Controller):
#     @http.route('/xmarts_l10n_pe_currency/xmarts_l10n_pe_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmarts_l10n_pe_currency/xmarts_l10n_pe_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmarts_l10n_pe_currency.listing', {
#             'root': '/xmarts_l10n_pe_currency/xmarts_l10n_pe_currency',
#             'objects': http.request.env['xmarts_l10n_pe_currency.xmarts_l10n_pe_currency'].search([]),
#         })

#     @http.route('/xmarts_l10n_pe_currency/xmarts_l10n_pe_currency/objects/<model("xmarts_l10n_pe_currency.xmarts_l10n_pe_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmarts_l10n_pe_currency.object', {
#             'object': obj
#         })
