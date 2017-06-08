# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Invoice Template Modifier Module',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Invoice Template Modifier Module',
    'description': """
    This module generates customization in invoice report 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'account',
        'invoice_date',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'report/customer_report_invoice.xml',
        'report/supplier_report_invoice.xml',
        'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}