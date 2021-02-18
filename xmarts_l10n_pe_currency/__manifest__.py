# -*- coding: utf-8 -*-
{
    'name': "Multimoneda para Perú",

    'summary': """
        Adecuaciones para uso de Odoo con multimoneda en Perú""",

    'description': """
        Adecuaciones para uso de Odoo con multimoneda en Perú
    """,

    'author': "Xmarts Peru",
    'website': "http://www.xmarts.com",

    'category': 'Xmarts/Localization',
    'version': '0.1',

    'depends': ['base','account'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/res_currency_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    "sequence": 2,
}
