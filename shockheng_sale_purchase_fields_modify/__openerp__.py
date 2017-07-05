# -*- coding: utf-8 -*-

{
    'name': 'Shockheng Sales Purchase Fields Modify',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Shockheng Sales Purchase Fields Modify',
    'description': """
    This module added shockheng fields modify in Sale Order and Purchase Order
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'account',
        'PaymentTerm_SO_Custom',
        'purchase_shockheng_modifier',
    ],
    'data': [
             'wizard/purchase_order_wiz_view.xml',
             'views/purchase_view.xml',
             'views/sale_order_view.xml',
             'views/product_view.xml',
             'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}