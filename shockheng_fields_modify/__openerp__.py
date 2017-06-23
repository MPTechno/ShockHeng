# -*- coding: utf-8 -*-

{
    'name': 'Shockheng Fields Modify',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Shockheng Fields Modify',
    'description': """
    This module added shockheng fields modify in My Follow-Ups and Warehouse
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'sale',
        'account_followup',
        'stock',
        'salesorder_modifier_module',
    ],
    'data': [
             'security/ir.model.access.csv',
             'data/product_type_view.xml',
             'views/res_partner_view.xml',
             'views/account_invoice_view.xml',
             'views/account_followup_invoice.xml',
             'views/product_type_config_view.xml',
             'views/stock_view.xml',
             'report/report_saleorder.xml',
             'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}