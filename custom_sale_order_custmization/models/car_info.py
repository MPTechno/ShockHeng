# -*- coding: utf-8 -*-
from openerp import api, fields, models

class car_brand(models.Model):
    _name = 'car.brand'

    name = fields.Char('Name')



class car_model(models.Model):
    _name = 'car.model'

    name = fields.Char('Name')
