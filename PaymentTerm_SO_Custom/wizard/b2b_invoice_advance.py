# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
from datetime import datetime

class b2b_advance_payment_inv(models.TransientModel):
    _inherit = "b2b.advance.payment.inv"
    _description = "B2B Payment Invoice"

    payment_terms_id = fields.Many2one('custom.payment.term','Payment Terms')

    @api.multi
    def create_b2b_invoices(self):
        invoice_obj = self.env['account.invoice']
        sale_obj = self.env['sale.order']
        sale_id = self._context.get('active_ids', [])
        sale_ids = sale_obj.browse(sale_id)
        res = super(b2b_advance_payment_inv, self).create_b2b_invoices()
        if res['res_id']:
            invoice_id = invoice_obj.browse(res['res_id'])
            invoice_id.update({'payment_terms_id': self.payment_terms_id.id})
            sale_ids.update({'payment_terms_id': self.payment_terms_id.id, 'b2c_payment_terms_id':[]})
        return res
