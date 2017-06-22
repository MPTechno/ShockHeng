# -*- coding: utf-8 -*-
import time
from datetime import datetime
from openerp import api, fields, models
from openerp.tools.translate import _


class Product_Pricelist_Report(models.TransientModel):

    _name = 'product.pricelist.report'
    _description = 'Print Product Price List Report of the given Date'

    start_date = fields.Datetime('Starting Date')
    end_date = fields.Datetime('Ending Date')
    type = fields.Selection([('b2b','B2B'),('b2c','B2C')])

    @api.multi
    def print_report(self):
        data = self.read([])[0]
        datas = {
             'ids': [],
             'model': 'sale.order',
             'form': data,
            }
        return self.env['report'].get_action(self, 'product_price_report_modify.b2b_and_b2c_product_price',
                                             data=datas)

