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
        xml_id = 'sale.view_order_tree'
        tree_view_id = self.env.ref(xml_id).id
        xml_id = 't20_sale.view_salesorder_proposal_form'
        # xml_id = 't20_core.view_analytic_code_budget_form'
        form_view_id = self.env.ref(xml_id).id
        return {
            'name': _('CONTRACTS'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'res_model': 'sale.order',
            'domain': [('job_id', 'in', self.ids), ('type', '=', 'prime'),
                       ('parent_id', '=', False)],
            'type': 'ir.actions.act_window',
            'context': {
                'default_job_id': self._ids[0],
                'default_type': 'prime',
            },
        }