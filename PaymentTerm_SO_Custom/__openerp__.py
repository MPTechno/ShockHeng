# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'PaymentTerm Sale Order Custom',
    'version': '1.2',
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
          'security/ir.model.access.csv',
          'data/account_data.xml',
          'wizard/b2b_invoice_advance.xml',
          'wizard/sale_make_invoice_advance.xml',
          'views/sale_view.xml',
          'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}