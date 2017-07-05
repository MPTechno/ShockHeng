# -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    payment_terms = fields.Many2one('custom.payment.term','Payment Mode', copy=False)


class hr_contract(models.Model):
    _inherit = 'hr.contract'
    
    overtime_pay = fields.Float('Overtime Pay')
