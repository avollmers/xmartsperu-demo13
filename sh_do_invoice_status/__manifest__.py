# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Delivery Order Invoice Status",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Warehouse",
    "summary": "Sale Order Invoice Status Module, Track Delivery Order Invoice Status, Invoice Partial Payment Status, Invoice Full Payment Status App, Print Invoice Status, DO Status,Invoice Payment Status Odoo",
    "description": """
This module helps to track the status of the invoice in the delivery order. You have the option to print invoice status in PDF and you have the option to show the amount in delivery order. You can filter like, partial payment or full payment. If partial payment is not done then the validate button will not display. This module shows the status of the invoice on the right side of your delivery order. You can print the delivery slip & picking operation with the status of the paid invoice.
 Delivery Order Invoice Status Odoo
 Invoice Status In Sale Order, Track Invoice Status In Delivery Order, Invoice Partial Payment Status Module, Invoice Full Payment Status, Print Invoice Status, Invoice Payment Status Odoo.
Sale Order Invoice Status Module, Track Delivery Order Invoice Status, Invoice Partial Payment Status, Invoice Full Payment Status App, Print Invoice Status, Invoice Payment Status Odoo

                    """,
    "version": "13.0.2",
    "depends": [
        "sale_management",
        "stock",
    ],
    "application": True,
    "data": [
        'views/res_config_setting_view.xml',
        'views/stock.xml',
        'views/report_picking_operation.xml',
            ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/0M9Rip0qrpE",
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
