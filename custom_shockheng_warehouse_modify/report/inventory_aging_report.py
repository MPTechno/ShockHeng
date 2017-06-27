# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw
from datetime import datetime

class inventory_aging_template_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(inventory_aging_template_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_inventory_details': self._get_inventory_details,
            'get_date': self._get_date,
        })

    def _get_date(self, order):
        start_date = datetime.strptime(order.start_date,"%Y-%m-%d %H:%M:%S")
        header_date = start_date.strftime("%d-%m-%Y %H:%M:%S")
        end_date = datetime.strptime(order.end_date,"%Y-%m-%d %H:%M:%S")
        header_end_date = end_date.strftime("%d-%m-%Y %H:%M:%S")
        sale_order_obj = self.pool.get('sale.order')
        account_move_obj = self.pool.get('stock.move')
        account_move_id = account_move_obj.search(self.cr, self.uid,[], limit=1)
        account_move_ids = account_move_obj.browse(self.cr, self.uid,account_move_id)
        sale_order_id = sale_order_obj.search(self.cr, self.uid, [('name','=', account_move_ids.origin)], limit=1)
        sale_order_ids = sale_order_obj.browse(self.cr, self.uid,sale_order_id)
        date_vals = {
                     'date_start': header_date,
                     'date_end': header_end_date,
                     'user_id': sale_order_ids.user_id
                     }
        return date_vals

    def _get_inventory_details(self, order):
        result = []
        def _get_rec(object):
            account_move_obj = self.pool.get('stock.move')
            account_move_id = account_move_obj.search(self.cr, self.uid,[
                                  ('date_expected', '>=', object.start_date),
                                  ('date_expected', '<=', object.end_date),
                                  ('picking_type_id.code','=','incoming'),
                                  ('state','=','done')], order="date_order asc")
            account_move_ids = account_move_obj.browse(self.cr, self.uid, account_move_id)
            parent_location = location = ''
            total = 0.00
            for line in account_move_ids:
                parent_location = str(line.location_dest_id.location_id.name)
                location = str(line.location_dest_id.name)
                date_expected = datetime.strptime(line.date_expected,"%Y-%m-%d %H:%M:%S").date()
                date_expected_date = date_expected.strftime("%d-%m-%Y")
                res = {}
                total += line.price_unit or 0.00
                res['date_of_movement'] = date_expected_date or ''
                res['product_number'] = line.product_number or ''
                res['product_id'] = line.product_id.name or ''
                res['quantity_on_hand'] = line.product_uom_qty or 0.00
                res['cost_price'] = line.price_unit or 0.00
                res['display_currency'] = line.company_id.currency_id.symbol
                res['current_location'] = location
                res['current_parent_location'] = parent_location
                result.append(res)
            result[0].update({'amount_total':total})
            return result
        children = _get_rec(order)
        return children


class inventory_aging_report_template_id(models.AbstractModel):
    _name = 'report.custom_shockheng_warehouse_modify.report_inventory_aging_template'
    _inherit = 'report.abstract_report'
    _template = 'custom_shockheng_warehouse_modify.report_inventory_aging_template'
    _wrapped_report_class = inventory_aging_template_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
