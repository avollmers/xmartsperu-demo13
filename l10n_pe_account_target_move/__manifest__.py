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

{
    'name' : 'Asientos Destino',
    'version' : '0.1',
    'author' : 'OPeru',
    'category' : 'Accounting',
    'summary': 'Asiento destino automaticos al publicar un asiento.',
    'description' : """
Cuentas destino automaticos al publicar un asiento.

    """,
    'website': 'http://odooperu.pe/page/contabilidad',
    'depends' : ['account'],
    'data': [
        'views/account_move_views.xml',
        'views/account_views.xml',
    ],
    'qweb' : [

    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'images': ['static/description/banner.png'],
    'live_test_url': 'http://operu.pe/manuales',
    'license': 'OPL-1',
    'support': 'soporte@operu.pe',
    'price': 9.00,
    'currency': 'EUR',
    'sequence': 2,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
