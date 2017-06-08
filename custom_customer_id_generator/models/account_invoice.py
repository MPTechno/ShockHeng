# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    customer_id = fields.Char('Customer Id', related='partner_id.customer_id', store=True)
