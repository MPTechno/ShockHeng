# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw
from datetime import datetime

class inherit_b2b_and_b2c_summary_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(inherit_b2b_and_b2c_summary_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_b2c_details': self.get_b2c_details,
            'get_date': self._get_date,
            'get_b2b_details': self.get_b2b_details
        })

    def _get_date(self, order):
        start_date = datetime.strptime(order.start_date,'%Y-%m-%d')
        header_date = start_date.strftime('%d-%m-%Y')
        end_date = datetime.strptime(order.end_date,'%Y-%m-%d')
        header_end_date = end_date.strftime('%d-%m-%Y')
        sale_order_obj = self.pool.get('sale.order')
        invoice_obj = self.pool.get('account.invoice')
        invoice_id = invoice_obj.search(self.cr, self.uid,[], limit=1)
        invoice_ids = invoice_obj.browse(self.cr, self.uid,invoice_id)
        sale_order_id = sale_order_obj.search(self.cr, self.uid, [('name','=', invoice_ids.origin)], limit=1)
        sale_order_ids = sale_order_obj.browse(self.cr, self.uid,sale_order_id)
        date_vals = {
                     'date_start': header_date,
                     'date_end': header_end_date,
                     'type': order.type,
                     'user_id': sale_order_ids.user_id
                     }
        return date_vals

    def get_b2c_details(self, order):
        result = []
        def _get_rec(object):
            invoice_obj = self.pool.get('account.invoice')
            invoice_id = invoice_obj.search(self.cr, self.uid,[('type','=','out_invoice'),
                                  ('date_invoice', '>=', object.start_date),
                                  ('date_invoice', '<=', object.end_date)])
            invoice_ids = invoice_obj.browse(self.cr, self.uid,invoice_id)
            total = 0.00
            for l in invoice_ids:
                res = {}
                total += l.amount_total
                res['date_invoice'] = l.date_invoice or 0.00
                res['amount_total'] = l.amount_total or 0.00
                res['invoice_number'] = l.number or ''
                res['b2c_payment_terms_id'] = l.b2c_payment_terms_id.name or ''
                res['display_currency'] = l.currency_id.symbol
                result.append(res)
            result[0].update({'total_sale':total})
            return result
        children = _get_rec(order)
        return children
    

    def get_b2b_details(self, order):
        result = []
        def _get_rec(object):
            invoice_obj = self.pool.get('account.invoice')
            sale_order_obj = self.pool.get('sale.order')
            invoice_id = invoice_obj.search(self.cr, self.uid,[('type','=','in_invoice'),
                                  ('date_invoice', '>=', object.start_date),
                                  ('date_invoice', '<=', object.end_date)])
            invoice_ids = invoice_obj.browse(self.cr, self.uid,invoice_id)
            total = 0.00
            for l in invoice_ids:
                res = {}
                total += l.amount_total
                res['date_invoice'] = l.date_invoice or 0.00
                res['amount_total'] = l.amount_total or 0.00
                res['invoice_number'] = l.number or ''
                res['payment_terms_id'] = l.payment_terms_id.name or ''
                res['display_currency'] = l.currency_id.symbol
                result.append(res)
            result[0].update({'total_outstanding':total})
            return result
        children = _get_rec(order)
        return children

class inherit_b2b_and_b2c_summary_report_template_id(models.AbstractModel):
    _name = 'report.custom_sale_order_custmization.report_b2b_and_b2c_total'
    _inherit = 'report.abstract_report'
    _template = 'custom_sale_order_custmization.report_b2b_and_b2c_total'
    _wrapped_report_class = inherit_b2b_and_b2c_summary_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
