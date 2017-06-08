# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class WizardCreateInvoiceLineItem(models.TransientModel):

    _name = 'wizard.create.invoice.line.item'

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_qty

    @api.model
    def _default_account(self):
        # XXX this gets the default account for the user's company,
        # it should get the default account for the invoice's company
        # however, the invoice's company does not reach this point
        if self._context.get('type') in ('out_invoice', 'out_refund'):
            return self.env['ir.property'].get('property_account_income_categ', 'product.category')
        else:
            return self.env['ir.property'].get('property_account_expense_categ', 'product.category')

    wizard_id = fields.Many2one('wizard.create.invoice.line', 'Wizard Invoice Line')
    product_id = fields.Many2one('product.product', string='Product',
        ondelete='restrict', index=True)
    name = fields.Text(string='Description')
    product_qty = fields.Float(string='Quantity', default=1, digits=dp.get_precision('Product Unit of Measure'))
    product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
    price_unit = fields.Float('Unit Price', digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float('Subtotal', compute='_compute_amount', store=True)
    account_id = fields.Many2one('account.account', string='Account',
        required=True, domain=[('type', 'not in', ['view', 'closed'])],
        default=_default_account,
        help="The income or expense account related to the selected product.")
    invoice_line_tax_id = fields.Many2many('account.tax',
        'wiz_account_invoice_line_tax', 'wiz_invoice_line_id', 'tax_id',
        string='Taxes')
    company_id = fields.Many2one('res.company','Company name')
    product_number = fields.Char(related="product_id.default_code", string='Product number')
    cost_price = fields.Float('Cost Price', digits=dp.get_precision('Product Price'))

    @api.onchange('product_id')
    def get_product_id(self, type='out_invoice'):
        product = self.product_id
        if product:
            if type in ('out_invoice', 'out_refund'):
                account = product.property_account_income or product.categ_id.property_account_income_categ
                self.account_id = account.id
            else:
                account = product.property_account_expense or product.categ_id.property_account_expense_categ
                self.account_id = account.id
            if type in ('out_invoice', 'out_refund'):
                if account:
                    taxes = product.taxes_id or account.tax_ids
                    self.invoice_line_tax_id = taxes.ids
                if product.description_sale:
                    self.name = product.description_sale or '/'
                else:
                    self.name = product.description or '/'
            else:
                if account:
                    taxes = product.supplier_taxes_id or account.tax_ids
                    self.invoice_line_tax_id = taxes.ids
                if product.description_purchase:
                    self.name = product.description_purchase or '/'
                else:
                    self.name = product.description or '/'
            self.price_unit = product.lst_price
            self.cost_price = product.standard_price
            self.product_uom = product.uom_id.id

class WizardCreateInvoiceLine(models.TransientModel):
    _name = 'wizard.create.invoice.line'

    wiz_invoice_order_line_item_ids = fields.One2many('wizard.create.invoice.line.item',
                                          'wizard_id', 'Invoice Lines')

    @api.multi
    def create_invoice_line(self):
        invoice_obj = self.env['account.invoice']
        active_ids = self._context.get('active_ids')
        invoice_id = invoice_obj.browse(active_ids)
        order_lines_lst = []
        tax_ids = []
        for record in self:
            vals = {}
            for line in record.wiz_invoice_order_line_item_ids:
                for tax in line.invoice_line_tax_id:
                    vals = {'invoice_line_tax_id': tax.ids}
                vals.update({
                    'name': line.name or '/',
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom.id,
                    'product_uom_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'cost_price': line.cost_price,
                    'company_id': line.company_id.id
                })
                order_lines_lst.append((0, 0, vals))
            if order_lines_lst:
                invoice_id.invoice_line = order_lines_lst
                