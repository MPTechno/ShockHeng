# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_description = fields.Text('Description')

account_invoice()


class product_product(models.Model):
    _inherit = 'product.product'

    brand = fields.Char('Brand')


product_product()