# -*- coding: utf-8 -*-

from openerp import api, fields, models
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
from datetime import datetime

class sale_advance_payment_inv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    b2c_payment_term = fields.Many2one('custom.payment.term','Payment Terms')

    @api.multi
    def create_invoices(self):
        invoice_obj = self.env['account.invoice']
        sale_obj = self.env['sale.order']
        sale_id = self._context.get('active_ids', [])
        sale_ids = sale_obj.browse(sale_id)
        sale_ids.update({'b2c_payment_terms_id': self.b2c_payment_term.id,'payment_terms_id':[]})
        return super(sale_advance_payment_inv, self).create_invoices()
