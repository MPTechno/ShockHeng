# -*- coding: utf-8 -*-
from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    customer_name = fields.Char('Customer Name')
    
    @api.multi
    @api.onchange('customer_name')
    def onchange_customer(self):
        partner_obj = self.env['res.partner']
        if self.customer_name:
            partner_id = partner_obj.search([('name','=',self.customer_name)])
            if partner_id:
                self.partner_id = partner_id.id
            else:
                values = {
                    'name': self.customer_name,
                    'user_id': self.user_id.id,
                    'type': 'invoice',
                    'customer': True,
                }
                customer = self.env['res.partner'].create(values)
                self.partner_id = customer.id
