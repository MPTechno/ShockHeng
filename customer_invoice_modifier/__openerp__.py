# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': ' Custom Customer Invoice Modifier',
    'version': '1.1',
    'category': 'Accounting',
    'summary': 'Customer Invoice Modifier',
    'description': """
    This module generates custom customer invoice modifier
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}