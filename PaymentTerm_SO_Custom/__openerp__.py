# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'PaymentTerm Sale Order Custom',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Custom Sales Order Customization',
    'description': """
    This module added payment terms in sale order 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'custom_sale_order_custmization',
    ],
    'data': [
          'data/account_data.xml',
          'views/sale_view.xml',
          'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}