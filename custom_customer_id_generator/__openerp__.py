# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': ' Custom Customer ID Generator',
    'version': '1.3',
    'category': 'Accounting',
    'summary': 'Unique ID for Customers',
    'description': """
    This module generates unique ID for Customers 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'account',
        'account_voucher',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/account_voucher_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}