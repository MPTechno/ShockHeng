# -*- coding: utf-8 -*-
from openerp import api, fields, models


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    car_brand_id = fields.Many2one(related='order_id.car_brand_id', string='Vehicle Brand', store=True)
    car_model_id = fields.Many2one(related='order_id.car_model_id', string='Vehicle Model', store=True)
    type = fields.Selection(related='order_id.type', string='Type', store=True)