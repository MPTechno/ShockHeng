# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_description = fields.Text('Description')
