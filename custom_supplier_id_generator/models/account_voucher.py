# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    
    supplier_id = fields.Char('Supplier Id', related='partner_id.supplier_id', store=True)
