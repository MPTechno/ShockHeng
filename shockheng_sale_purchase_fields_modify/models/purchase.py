# -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the request for quotation and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'send_rfq')
        return self.pool['report'].get_action(cr, uid, ids, 'purchase_shockheng_modifier.custom_purchase_order_report_template', context=context)

    payment_terms = fields.Many2one('custom.payment.term','Payment Terms', copy=False)