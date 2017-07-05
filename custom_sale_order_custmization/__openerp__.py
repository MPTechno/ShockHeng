# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Sale Order Modifier Module',
    'version': '1.6',
    'category': 'Sale',
    'summary': 'Custom Sales Order Customization',
    'description': """
    This module generates modification in sale order 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'sale',
        'sale_stock',
        'account',
        'hr',
        'salesorder_modifier_module',
        'custom_partial_invoice_payment',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/b2b_invoice_advance.xml',
        'wizard/b2b_and_b2c_summary_view.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
        'views/account_invoice_view.xml',
        'views/car_info_view.xml',
        'views/car_menu.xml',
        'report/b2b_report_invoice.xml',
        'report/b2c_report_invoice.xml',
        'report/b2b_and_b2c_summary_report_view.xml',
        'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}