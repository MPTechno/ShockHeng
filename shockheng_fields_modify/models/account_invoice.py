# -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('partner_id')
    def _get_amounts_and_date(self):
        '''
        Function that computes values for the followup functional fields. Note that 'payment_amount_due'
        is similar to 'credit' field on res.partner except it filters on user's company.
        '''
        company = self.company_id
        for invoice in self:
            worst_due_date = False
            amount_due = 0.0
            for aml in invoice.partner_id.unreconciled_aml_ids:
                if (aml.company_id.id == company.id):
                    date_maturity = aml.date_maturity or aml.date
                    if not worst_due_date or date_maturity < worst_due_date:
                        worst_due_date = date_maturity
                    amount_due += aml.result
            invoice.update({'payment_amount_due': amount_due}) 

    car_name = fields.Char('Car Name', related='partner_id.car_name', store=True)
    car_brand = fields.Char('Car brand', related='partner_id.car_brand_no', store=True)
    car_model = fields.Char('Car Model', related='partner_id.model_no', store=True)
    payment_amount_due = fields.Float(compute='_get_amounts_and_date', string='Amount Due', store = False)
