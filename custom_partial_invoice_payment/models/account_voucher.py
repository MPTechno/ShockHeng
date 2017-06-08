# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    
    @api.multi
    def button_proforma_voucher(self):
        res = super(account_voucher,self).button_proforma_voucher()
        invoice_line_obj = self.env['account.invoice.line']
        for voucher in self:
            voucher.signal_workflow('proforma_voucher')
            context = self._context
            if context.get('invoice_line_ids'):
                invoice_line_ids = invoice_line_obj.browse(context.get('invoice_line_ids'))
                for line in invoice_line_ids:
                    line.update({'state':'paid'})
        return res
