# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    vehicle_no = fields.Char('Vehicle No')
