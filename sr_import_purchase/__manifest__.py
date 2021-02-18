# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': "Import Purchase Orders from Excel/CSV",
    'version': "13.0.0.0",
    'summary': "This module helps you to import Purchase Orders from Excel/CSV",
    'category': 'Purchases',
    'description': """
        Using this module Purchase Orders is imported using excel/CSV sheets
    import Purchase Orders using csv 
    import Purchase Orders using xls
    import bulk purchase from Excel file
    import bulk purchase from CSV file
    Import purchase order lines from CSV or Excel file
    Add PO from Excel
    Add PO from CSV
    import PO
    
    """,
    'author': "Sitaram",
    'website': "sitaramsolutions.in",
    'depends': ['base', 'purchase'],
    'data': [
        'wizard/import_purchase.xml',
        
    ],
    'live_test_url':'https://youtu.be/fPgZYHlavXA',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
