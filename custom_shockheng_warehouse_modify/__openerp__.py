# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Shockheng Warehouse Module',
    'version': '1.2',
    'category': 'Sale',
    'summary': 'Custom Shockheng Warehouse Module',
    'description': """
    This module generates modification in warehouse for Shockheng 
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'shockheng_fields_modify',
    ],
    'data': [
             'wizard/inventory_aging_report_view.xml',
             'report/inventory_aging_report_view.xml',
             'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}