# -*- coding: utf-8 -*-
from openerp import api, fields, models

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids,
                          pricelist, 
                          product,
                          qty=0,
                          uom=False,
                          qty_uos=0,
                          uos=False,
                          name='',
                          partner_id=False,
                          lang=False,
                          update_tax=True,
                          date_order=False,
                          packaging=False,
                          fiscal_position=False,
                          flag=False, context=None):
        """
        check product description set into the sale order line
        """
        res = super(sale_order_line,self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        if product:
            product_res = self.pool.get('product.product').browse(cr, uid, product, context=context)
            if product_res.description:
                res['value'].update({'name':product_res.description})
            else:
                res['value'].update({'name':product_res.description_sale})
        return res