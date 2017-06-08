# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    supplier_id = fields.Char('Supplier Id', related='partner_id.supplier_id', store=True)
