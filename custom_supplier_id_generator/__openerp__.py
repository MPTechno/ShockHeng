# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': ' Custom Supplier ID Generator',
    'version': '1.3',
    'category': 'Accounting',
    'summary': 'Unique ID for Supplier',
    'description': """
    This module generates unique ID for Supplier 
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