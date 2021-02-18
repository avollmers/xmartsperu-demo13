# -*- coding: utf-8 -*-
{
    'name': "Tipo de cambio",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Xmarts",
    'website': "http://www.xmarts.com",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account','l10n_pe'],

    'data': [
        'views/res_currency_view.xml',
        'data/update.xml',
        'data/setting_res_lang.xml',
        'views/res_config_settings.xml',
        'data/service_cron_data.xml'
    ],

}
