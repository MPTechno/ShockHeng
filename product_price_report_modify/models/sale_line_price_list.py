# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class sale_order_line_product_pricelist(models.Model):
    _name = "sale.order.line.product.pricelist"
    _description = "Sale OrderLine Product Pricelist"

    @api.multi
    def _pricelist_type_get(self):
        pricelist_type_obj = self.env['product.pricelist.type']
        pricelist_type_ids = pricelist_type_obj.search([], order='name')
        pricelist_types = pricelist_type_ids.read(['key','name'])
        res = []
        for type in pricelist_types:
            res.append((type['key'],type['name']))
        return res

    name = fields.Char('Pricelist Name', translate=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the pricelist without removing it.")
    version_id = fields.One2many('product.pricelist.version', 'pricelist_id', 'Pricelist Versions', copy=True)
    currency_id = fields.Many2one('res.currency', 'Currency')
    company_id = fields.Many2one('res.company', 'Company')
    type = fields.Selection(_pricelist_type_get, 'Pricelist Type')


    @api.multi
    def create_product_pricelist(self):
        version_lst = []
        price_list_obj = self.env['product.pricelist']
        for product in self:
            for version in product.version_id:
                version_lst.append(version.id)
            product_pricelist = price_list_obj.create({
                'name': product.name,
                'type': product.type,
                'currency_id': product.currency_id.id,
                'company_id': product.company_id.id,
                'version_id': [(6, 0 , version_lst)],
            })
            print 'product_pricelist===========',product_pricelist
            xml_id = 'product.product_pricelist_view_tree'
            tree_view_id = self.env.ref(xml_id).id
            xml_id = 'product.product_pricelist_view'
            form_view_id = self.env.ref(xml_id).id
            return {
                'name': _('Price List'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'res_id': product_pricelist.id,
                'res_model': 'product.pricelist',
                'type': 'ir.actions.act_window',
                }
