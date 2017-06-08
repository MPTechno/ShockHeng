# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': ' Custom Partial Payment From Invoice',
    'version': '1.1',
    'category': 'Project',
    'summary': 'Custom Partial Payment From Invoice',
    'description': """
    This module generates partial payment From Invoice 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'account',
        'account_voucher',
    ],
    'data': [
        'wizard/account_invoice_add_line_view.xml',
        'views/account_invoice_view.xml',
        'report/report_account_invoice.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}