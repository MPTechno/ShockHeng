# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': ' Custom Record Filter For Invoice Date',
    'version': '1.1',
    'category': 'Project',
    'summary': 'Custom Record Filter For Invoice Date',
    'description': """
    This module generates record filter for invoice date 
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