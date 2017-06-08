# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Picking Wave Template Modifier Module',
    'version': '1.1',
    'category': 'Purchase',
    'summary': 'Stock Picking Wave Template Modifier Module',
    'description': """
    This module generates customization in stock picking wave template modifier module.
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'stock_picking_wave',
        'sg_account',
    ],
    'data': [
        'report/report_picking_wave.xml',
        'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}