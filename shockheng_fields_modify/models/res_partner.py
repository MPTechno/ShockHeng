# -*- coding: utf-8 -*-
from openerp import api, fields, models

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    car_name = fields.Char('Car Name')

