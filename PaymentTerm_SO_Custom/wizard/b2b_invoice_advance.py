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
    _inherit = "b2b.advance.payment.inv"
    _description = "B2B Payment Invoice"

    @api.multi
    def create_b2b_invoices(self):
        invoice_obj = self.env['account.invoice']
        sale_obj = self.env['sale.order']
        sale_id = self._context.get('active_ids', [])
        sale_ids = sale_obj.browse(sale_id)
        res = super(b2b_advance_payment_inv, self).create_b2b_invoices()
        if res['res_id']:
            invoice_id = invoice_obj.browse(res['res_id'])
            invoice_id.update({'payment_terms_id': sale_ids.payment_terms_id.id})
