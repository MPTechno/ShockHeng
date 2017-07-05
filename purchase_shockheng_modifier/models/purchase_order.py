# -*- coding: utf-8 -*-
from openerp import api, fields, models

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'
    
    date = fields.Date('Date', default=fields.Date.context_today)
    vehicle_no = fields.Char('Vehicle No')
