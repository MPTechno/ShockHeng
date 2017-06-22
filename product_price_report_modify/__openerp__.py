# -*- coding: utf-8 -*-

{
    'name': 'Product Price Report Modify',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Product Price Report Modify',
    'description': """
    This module added product price report in sale order 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'custom_sale_order_custmization',
    ],
    'data': [
             'wizard/b2b_and_b2c_product_view.xml',
             'report/b2b_and_b2c_product_report_view.xml',
             'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}