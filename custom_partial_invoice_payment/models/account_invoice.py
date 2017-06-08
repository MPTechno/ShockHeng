# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp

class Account_Invoice_Line(models.Model):
    _inherit = 'account.invoice.line'
    
    amount_check = fields.Boolean('Check')
    state = fields.Selection([
            ('paid','Paid'),
            ('unpaid','UnPaid'),
        ], default='unpaid', string='Status')
    cost_price = fields.Float('Cost Price', digits=dp.get_precision('Product Price'))
    product_number = fields.Char(related="product_id.default_code", string='Product Number')
    invoice_state = fields.Selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Pro-forma' when invoice is in Pro-forma status,invoice does not have an invoice number.\n"
             " * The 'Open' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_line = fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines',
               readonly=False, copy=True)

    @api.multi
    def invoice_pay_customer(self):
        if not self._ids: return []
        dummy, view_id = self.env['ir.model.data'].get_object_reference('account_voucher', 'view_vendor_receipt_dialog_form')

        line_lst = []
        amount = 0.00
        inv = self
        for line in self.invoice_line:
            if line.amount_check and line.state != 'paid':
                line_lst.append(line.id)
                amount += line.price_subtotal
                inv.residual = amount
        return {
            'name':_("Pay Invoice"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'payment_expected_currency': self.currency_id.id,
                'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(self.partner_id).id,
                'default_amount': self.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                'default_reference': inv.name,
                'close_after_process': True,
                'invoice_type': inv.type,
                'invoice_id': inv.id,
                'default_type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
                'type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
                'invoice_line_ids': line_lst
            }
        }

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            invoice.state = 'open'
            for line in invoice.invoice_line:
                line.invoice_state = 'open'
        return True

    @api.multi
    def write(self, vals):
        for invoice in self:
            if invoice.state == 'paid':
                for line in invoice.invoice_line:
                    line.update({'state':'paid'})
        return super(AccountInvoice, self).write(vals)