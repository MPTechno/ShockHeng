# -*- coding: utf-8 -*-
from openerp import api, fields, models

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    supplier_id = fields.Char('Supplier ID', select=True)
    related_supplier_id = fields.Many2one('res.partner','Supplier')

    _sql_constraints = [
        ('supplier_id_uniq', 'unique(supplier_id)', 'Supplier Id already exists!')
    ]

    @api.multi
    @api.onchange('supplier_id')
    def onchange_supplier_id(self):
        if self.supplier_id:
            partner_obj = self.env['res.partner']
            partner_id = partner_obj.search([('supplier_id','=',self.supplier_id)])
            self.related_supplier_id = partner_id.id