# -*- coding: utf-8 -*-
from openerp import api, fields, models

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    customer_id = fields.Char('Customer ID', select=True)
    related_customer_id = fields.Many2one('res.partner','Customer')

    _sql_constraints = [
        ('customer_id_uniq', 'unique(customer_id)', 'Customer Id already exists!')
    ]

    @api.multi
    @api.onchange('customer_id')
    def onchange_customer_id(self):
        if self.customer_id:
            partner_obj = self.env['res.partner']
            partner_id = partner_obj.search([('customer_id','=',self.customer_id)])
            self.related_customer_id = partner_id.id