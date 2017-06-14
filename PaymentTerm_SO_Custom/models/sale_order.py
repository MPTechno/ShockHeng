# -*- coding: utf-8 -*-
from openerp import api, fields, models

class sale_order(models.Model):
    _inherit = 'sale.order'

    payment_terms_id = fields.Many2one('custom.payment.term','Payment Terms')


class custom_payment_term(models.Model):
    _name = "custom.payment.term"
    _description = "Payment Term"
    name = fields.Char('Payment Term', translate=True, required=True)
    note = fields.Text('Description', translate=True)
