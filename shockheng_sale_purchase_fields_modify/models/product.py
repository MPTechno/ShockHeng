# -*- coding: utf-8 -*-
from openerp import api, fields, models

class product_template(models.Model):
    _inherit = 'product.template'

    @api.model
    def default_get(self, fields_list):
        defaults = super(product_template, self).default_get(fields_list)
        if self._context.get('search_default_sale_ok'):
            defaults.update({'sale_ok':True,'purchase_ok':False})
        if self._context.get('search_default_purchase_ok'):
            defaults.update({'purchase_ok':True,'sale_ok':False})
        return defaults


class product_product(models.Model):
    _inherit = 'product.product'

    @api.model
    def default_get(self, fields_list):
        defaults = super(product_product, self).default_get(fields_list)
        if self._context.get('search_default_sale_ok'):
            defaults.update({'sale_ok':True,'purchase_ok':False})
        if self._context.get('search_default_purchase_ok'):
            defaults.update({'purchase_ok':True,'sale_ok':False})
        return defaults