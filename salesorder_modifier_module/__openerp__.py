# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Salesorder Modifier Module',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Sales Order Customization',
    'description': """
    This module generates customization in sale order 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'data/res_group_view.xml',
        'views/sale_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}