# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Invoice Date Field',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Added Date Field in Invoice.',
    'description': """
    This module generates added date field in Invoice 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}