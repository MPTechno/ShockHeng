# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw
from datetime import datetime

class b2b_and_b2c_product_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(b2b_and_b2c_product_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_b2c_product_details': self.get_b2c_product_details,
            'get_date': self._get_date,
            'get_b2b_product_details': self.get_b2b_product_details
        })

    def _get_date(self, order):
        start_date = datetime.strptime(order.start_date,"%Y-%m-%d %H:%M:%S")
        header_date = start_date.strftime("%d-%m-%Y %H:%M:%S")
        end_date = datetime.strptime(order.end_date,"%Y-%m-%d %H:%M:%S")
        header_end_date = end_date.strftime("%d-%m-%Y %H:%M:%S")
        sale_order_obj = self.pool.get('sale.order')
        sale_order_id = sale_order_obj.search(self.cr, self.uid, [], limit=1)
        sale_order_ids = sale_order_obj.browse(self.cr, self.uid,sale_order_id)
        date_vals = {
                     'date_start': header_date,
                     'date_end': header_end_date,
                     'type': order.type,
                     'user_id': sale_order_ids.user_id
                     }
        return date_vals

    def get_b2c_product_details(self, order):
        result = []
        def _get_rec(object):
            sale_order_obj = self.pool.get('sale.order')
            sale_order_id = sale_order_obj.search(self.cr, self.uid,[('type','=','b2c'),
                                  ('date_order', '>=', object.start_date),
                                  ('date_order', '<=', object.end_date)])
            sale_order_ids = sale_order_obj.browse(self.cr, self.uid,sale_order_id)
            total = 0.00
            for l in sale_order_ids:
                res = {}
                total += l.amount_total
                res['car_brand'] = l.car_brand_id.name
                res['car_model'] = l.car_model_id.name
                res['order_line'] = l.order_line
                res['display_currency'] = l.currency_id.symbol
                result.append(res)
            result[0].update({'total_sale':total})
            return result
        children = _get_rec(order)
        return children
    

    def get_b2b_product_details(self, order):
        result = []
        def _get_rec(object):
            sale_order_obj = self.pool.get('sale.order')
            sale_order_id = sale_order_obj.search(self.cr, self.uid,[('type','=','b2b'),
                                  ('date_order', '>=', object.start_date),
                                  ('date_order', '<=', object.end_date)])
            sale_order_ids = sale_order_obj.browse(self.cr, self.uid,sale_order_id)
            total = 0.00
            for l in sale_order_ids:
                res = {}
                total += l.amount_total
                res['car_brand'] = l.car_brand_id.name
                res['car_model'] = l.car_model_id.name
                res['order_line'] = l.order_line
                res['display_currency'] = l.currency_id.symbol
                result.append(res)
            result[0].update({'amount_total_total':total})
            return result
        children = _get_rec(order)
        return children

class b2b_and_b2c_product_report_template_id(models.AbstractModel):
    _name = 'report.product_price_report_modify.b2b_and_b2c_product_price'
    _inherit = 'report.abstract_report'
    _template = 'product_price_report_modify.b2b_and_b2c_product_price'
    _wrapped_report_class = b2b_and_b2c_product_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
