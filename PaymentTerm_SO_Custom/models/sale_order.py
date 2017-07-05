# -*- coding: utf-8 -*-
from openerp import api, fields, models

class sale_order(models.Model):
    _inherit = 'sale.order'

    payment_terms_id = fields.Many2one('custom.payment.term','Payment Terms', copy=False)
    b2c_payment_terms_id = fields.Many2one('custom.payment.term','Payment Terms', copy=False)

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=None)
        if res:
            res.update({
                  'b2c_payment_terms_id': order.b2c_payment_terms_id.id,
            })
        return res


class custom_payment_term(models.Model):
    _name = "custom.payment.term"
    _description = "Payment Term"
    name = fields.Char('Payment Term', translate=True, required=True)
    note = fields.Text('Description', translate=True)
