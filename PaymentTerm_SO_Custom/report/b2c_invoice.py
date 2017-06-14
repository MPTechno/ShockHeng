# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw

class b2c_invoice_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(b2c_invoice_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_b2c_details': self.get_b2c_details,
        })

    
    def get_b2c_details(self, order):
        result = []

        def _get_rec(object):
            invoice_obj = self.pool.get('account.invoice')
            invoice_id = invoice_obj.search(self.cr, self.uid,[('id','in',object.invoice_ids.ids),('type','=','out_invoice')]) 
            invoice_ids = invoice_obj.browse(self.cr, self.uid,invoice_id)
            for l in invoice_ids:
                res = {}
                res['partner'] = l.partner_id.name
                res['partner_id'] = l.partner_id
                res['number'] = l.number
                res['date_invoice'] = l.date_invoice
                res['payment_term'] = l.payment_term.name
                res['amount_total'] = l.amount_total
                res['invoice_line'] = l.invoice_line
                res['display_currency'] = l.currency_id.symbol
                res['customer_email'] = l.customer_email
                res['customer_contact_no'] = l.customer_contact_no
                result.append(res)
            return result
        children = _get_rec(order)
        return children

class report_b2c_invoice(models.AbstractModel):
    _name = 'report.custom_sale_order_custmization.custom_b2c_invoice_template'
    _inherit = 'report.abstract_report'
    _template = 'custom_sale_order_custmization.custom_b2c_invoice_template'
    _wrapped_report_class = b2c_invoice_report