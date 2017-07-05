# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Shockheng Modifier Module',
    'version': '1.1',
    'category': 'Purchase',
    'summary': 'Purchase Shockheng Modifier Module',
    'description': """
    This module generates customization in Purchase Shockheng Module
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'report/report_purchase_order.xml',
        'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}