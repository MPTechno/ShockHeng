# -*- coding: utf-8 -*-
import time
from datetime import datetime
from openerp import api, fields, models
from openerp.tools.translate import _


class Outstanding_Payment_Report(models.TransientModel):

    _name = 'outstanding.payment.report'
    _description = 'Print Outstanding Report of the given Date'

    start_date = fields.Datetime('Starting Date')
    end_date = fields.Datetime('Ending Date')

    @api.multi
    def print_report(self):
        data = self.read([])[0]
        datas = {
             'ids': [],
             'model': 'purchase.order',
             'form': data,
            }
        return self.env['report'].get_action(self, 'custom_fields_shockheng_modify.report_purchase_outstanding_total',
                                             data=datas)

