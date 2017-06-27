# -*- coding: utf-8 -*-
import time
from datetime import datetime
from openerp import api, fields, models
from openerp.tools.translate import _


class InventoryAgingReport(models.TransientModel):

    _name = 'inventory.aging.report'
    _description = 'Print Inventory Aging Report of the given Date'

    start_date = fields.Datetime('Starting Date')
    end_date = fields.Datetime('Ending Date')

    @api.multi
    def print_report(self):
        data = self.read([])[0]
        datas = {
             'ids': [],
             'model': 'stock.move',
             'form': data,
            }
        return self.env['report'].get_action(self, 'custom_shockheng_warehouse_modify.report_inventory_aging_template',
                                             data=datas)

