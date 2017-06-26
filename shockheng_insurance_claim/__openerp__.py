# -*- coding: utf-8 -*-

{
    'name': 'Shockheng Insurance Claims',
    'version': '1.1',
    'category': 'Sale',
    'summary': 'Shockheng Insurance Claims',
    'description': """
    This module added insurance claims
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'sale',
        'fleet',
    ],
    'data': [
            'security/ir.model.access.csv',
            'data/vehicle_insurance_data.xml',
            'views/vehicle_insurance_view.xml',
            'report/report_insurence_claim.xml',
            'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}