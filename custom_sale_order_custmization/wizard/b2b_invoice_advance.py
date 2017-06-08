##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
from datetime import datetime

class b2b_advance_payment_inv(models.TransientModel):
    _name = "b2b.advance.payment.inv"
    _description = "B2B Payment Invoice"

    partner_id = fields.Many2one('res.partner','Supplier', domain=[('supplier','=',True)])

    @api.multi
    def create_b2b_invoices(self):
        """
        Create the invoice based on progress bill and billing line.
        """
        inv_obj = self.env['account.invoice']
        sale_obj = self.env['sale.order']
        ir_property_obj = self.env['ir.property']
        sale_id = self._context.get('active_ids', [])
        sale_ids = sale_obj.browse(sale_id)
        wizard = self
        xml_id = 'account.invoice_supplier_form'
        view_id = self.env.ref(xml_id).id
        invoice_ids = []
        vals = {}
        for sale in sale_ids:
            inv_lines = []
            for line in sale.order_line:
                product = line.product_id
                account_id = False
                if product.id:
                    account_id = product.property_account_expense.id
                if not account_id:
                    prop = ir_property_obj.get('property_account_expense_categ', 'product.category')
                    account_id = prop and prop.id or False
                if not account_id:
                    raise Warning(_('There is no income account defined for '
                        'this product: "%s". You may have to install a chart '
                        'of account from Accounting app, settings menu.') % \
                        (product.name,))
                # construct invoice lines
                if product.default_code:
                    vals = {'name': '[' + str(product.default_code) + ']' +' '+ str(product.name)}
                else:
                    vals = {'name': str(product.name)}
                vals.update({
                        'origin': sale.name,
                        'account_id': account_id,
                        'price_unit': line.price_unit,
                        'quantity': line.product_uom_qty,
                        'discount': 0.0,
                        'uom_id': product.uom_id.id,
                        'product_id': product.id,
                        'invoice_line_tax_id': [(6, 0, [x.id for x in product.taxes_id])],
                        'account_analytic_id': sale.project_id and sale.project_id.id or False,
                })
                inv_lines.append((0, 0, vals))
            # create invoice
            customer = wizard.partner_id
            date = datetime.strptime(sale.date_order, "%Y-%m-%d %H:%M:%S").date()
            invoice = inv_obj.create({
                'name': sale.client_order_ref or sale.name,
                'date_invoice': date,
                'origin': sale.name,
                'type': 'in_invoice',
                'reference': False,
                'account_id': customer.property_account_payable.id,
                'partner_id': customer.id,
                'currency_id': sale.currency_id.id,
                'invoice_line': inv_lines,
                'payment_term': sale.payment_term.id,
                'fiscal_position': sale.fiscal_position.id or sale.partner_id.property_account_position.id,
                'b2b_invoice':True,
            })
            sale.update({'type':'b2b','b2b_invoice':True,'supp_invoice_ids':[(6, 0, invoice.ids)]})
            invoice_ids.append(invoice.id)
            return {
                'name': _('Supplier Invoice'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'res_id': invoice and invoice.id or False,
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
            }
