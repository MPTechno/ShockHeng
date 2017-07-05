# -*- coding: utf-8 -*-
import time
from datetime import datetime
from openerp import api, fields, models
from openerp.tools.translate import _


class Invoice_Total_Summary(models.TransientModel):

    _name = 'invoice.total.summary'
    _description = 'Print Total Summary Report of the given Date'

    start_date = fields.Date('Starting Date')
    end_date = fields.Date('Ending Date')
    type = fields.Selection([('b2b','B2B'),('b2c','B2C')])

    @api.multi
    def print_report(self):
        data = self.read([])[0]
        datas = {
             'ids': [],
             'model': 'account.invoice',
             'form': data,
            }
        return self.env['report'].get_action(self, 'custom_sale_order_custmization.report_b2b_and_b2c_total',
                                             data=datas)

