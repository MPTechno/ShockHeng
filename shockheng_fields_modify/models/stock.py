# -*- coding: utf-8 -*-
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class stock_move(models.Model):
    _inherit = 'stock.move'

    product_type = fields.Many2one('stock.product.type','Product Type')
    date_order = fields.Date('Date Ordered')
    product_number = fields.Char(related="product_id.default_code", string='Product Number')
    price_unit = fields.Float('Price', digits=dp.get_precision('Product Price'), default=0.0)

    @api.model
    def default_get(self, fields_list):
        res = super(stock_move, self).default_get(fields_list)
        stock_picking = self.env['stock.picking.type'].search([('code','=','incoming')], limit=1)
        if stock_picking:
            res.update({'picking_type_id': stock_picking.id})
        return res

class stock_product_type(models.Model):
    _name = 'stock.product.type'
    
    name = fields.Char('Name')