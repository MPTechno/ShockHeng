# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw
from datetime import datetime

class purchase_outstanding_summary_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(purchase_outstanding_summary_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_outstanding_invoices_details': self._get_outstanding_invoices_details,
            'get_date': self._get_date,
        })

    def _get_date(self, order):
        start_date = datetime.strptime(order.start_date,"%Y-%m-%d %H:%M:%S")
        header_date = start_date.strftime("%d-%m-%Y %H:%M:%S")
        end_date = datetime.strptime(order.end_date,"%Y-%m-%d %H:%M:%S")
        header_end_date = end_date.strftime("%d-%m-%Y %H:%M:%S")
        purchase_order_obj = self.pool.get('purchase.order')
        invoice_obj = self.pool.get('account.invoice')
        purchase_order_id = purchase_order_obj.search(self.cr, self.uid, [], limit=1)
        purchase_order_ids = purchase_order_obj.browse(self.cr, self.uid,purchase_order_id)
        date_vals = {
                     'date_start': header_date,
                     'date_end': header_end_date,
                     'company_id': purchase_order_ids.company_id
                     }
        return date_vals

    def _get_outstanding_invoices_details(self, order):
        result = []
        def _get_rec(object):
            purchase_order_obj = self.pool.get('purchase.order')
            invoice_obj = self.pool.get('account.invoice')
            purchase_id = purchase_order_obj.search(self.cr, self.uid,[
                                  ('date_order', '>=', object.start_date),
                                  ('date_order', '<=', object.end_date),
                                  ('state','=','approved')])
            purchase_ids = purchase_order_obj.browse(self.cr, self.uid,purchase_id)
            amount_paid = 0.00
            inv_ids = []
            for purchase in purchase_ids:
                inv_ids+= [invoice.id for invoice in purchase.invoice_ids]
            if inv_ids:
                invoice_ids = invoice_obj.browse(self.cr, self.uid,inv_ids)
                for invoice in invoice_ids:
                    res = {}
                    header_date_invoice = ''
                    if invoice.date_invoice:
                        date_invoice = datetime.strptime(invoice.date_invoice,"%Y-%m-%d")
                        header_date_invoice = date_invoice.strftime("%d-%m-%Y")
                    amount_paid = invoice.amount_total - invoice.residual
                    res['date_invoice'] = header_date_invoice or ''
                    res['total_amount'] = invoice.amount_total or 0.00
                    res['amount_payable'] = invoice.residual or 0.00
                    res['amount_paid'] = amount_paid or 0.00
                    res['invoice_number'] = invoice.number or ''
                    res['display_currency'] = invoice.currency_id.symbol
                    result.append(res)
                return result
        children = _get_rec(order)
        return children


class purchase_outstanding_summary_report_template(models.AbstractModel):
    _name = 'report.custom_fields_shockheng_modify.report_purchase_outstanding_total'
    _inherit = 'report.abstract_report'
    _template = 'custom_fields_shockheng_modify.report_purchase_outstanding_total'
    _wrapped_report_class = purchase_outstanding_summary_report

