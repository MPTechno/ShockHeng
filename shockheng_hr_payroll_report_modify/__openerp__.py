# -*- coding: utf-8 -*-

{
    'name': 'Shockheng HR-Payroll Report Modify',
    'version': '1.1',
    'category': 'HR-Payroll',
    'summary': 'Shockheng HR-Payroll Report Modify',
    'description': """
    This module added shockheng hr payroll report modify
    """,
    'author': 'HashMicro / GeminateCS',
    'website': 'www.hashmicro.com', 
    'depends': [
        'hr_payroll',
        'hr_contract',
        'l10n_sg_hr_payroll',
        'PaymentTerm_SO_Custom',
    ],
    'data': [
             'views/payslip_view.xml',
             'report/hr_payslip_report.xml',
             'report/report_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}