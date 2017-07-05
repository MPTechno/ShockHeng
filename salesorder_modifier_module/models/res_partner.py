# -*- coding: utf-8 -*-
from openerp import api, fields, models

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    vehicle_no = fields.Char('Vehicle No')
    car_brand_no = fields.Char("Vehicle's Brand")
    model_no = fields.Char('Vehicle Model')

