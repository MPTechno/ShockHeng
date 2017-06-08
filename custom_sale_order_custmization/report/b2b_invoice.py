# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw

class b2b_invoice_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(b2b_invoice_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_b2b_details': self.get_b2b_details,
        })

    
    def get_b2b_details(self, order):
        result = []

        def _get_rec(object):
            invoice_obj = self.pool.get('account.invoice')
            invoice_id = invoice_obj.search(self.cr, self.uid,[('id','in',object.supp_invoice_ids.ids),('type','=','in_invoice')]) 
            invoice_ids = invoice_obj.browse(self.cr, self.uid,invoice_id)
            for l in invoice_ids:
                res = {}
                res['partner'] = l.partner_id.name or ''
                res['partner_id'] = l.partner_id or ''
                res['number'] = l.number or ''
                res['date_invoice'] = l.date_invoice or ''
                res['payment_term'] = l.payment_term.name or ''
                res['amount_total'] = l.amount_total or 0.00
                res['invoice_line'] = l.invoice_line or False
                res['display_currency'] = l.currency_id.symbol or False
                result.append(res)
            return result
        children = _get_rec(order)
        return children

class report_b2b_invoice(models.AbstractModel):
    _name = 'report.custom_sale_order_custmization.custom_b2b_invoice_template'
    _inherit = 'report.abstract_report'
    _template = 'custom_sale_order_custmization.custom_b2b_invoice_template'
    _wrapped_report_class = b2b_invoice_report