# -*- coding: utf-8 -*-
from openerp import api, fields, models

class sale_order(models.Model):
    _inherit = 'sale.order'

    car_brand_id = fields.Many2one('car.brand','Car Brand')
    car_model_id = fields.Many2one('car.model','Car Model')
    vehicle_number = fields.Char('Vehicle Number')
    b2b_invoice = fields.Boolean('B2B Invoice', copy=False)
    b2c_invoice = fields.Boolean('B2C Invoice', copy=False)
    state = fields.Selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True)
    type = fields.Selection([('b2b','B2B'),('b2c','B2C')])
    supp_invoice_ids = fields.Many2many('account.invoice', 'sale_order_supplier_invoice_rel', 'order_id', 'supp_invoice_id', 'Invoices', readonly=True, copy=False, 
                                        help="This is the list of invoices that have been generated for this sales order. The same sales order may have been invoiced in several times (by line for example).")

    @api.multi
    def confirm_quotation(self):
        for on in self:
            on.state = 'sent'

    def print_b2c_invoice(self, cr, uid, ids, context=None):
        return self.pool['report'].get_action(cr, uid, ids, 'custom_sale_order_custmization.custom_b2c_invoice_template', context=context)

    def print_b2b_invoice(self, cr, uid, ids, context=None):
        return self.pool['report'].get_action(cr, uid, ids, 'custom_sale_order_custmization.custom_b2b_invoice_template', context=context)

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=None)
        if res:
            order.update({'type': 'b2c','b2c_invoice':True})
        return res

    def action_b2b_view_invoice(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #compute the number of invoices to display
        inv_ids = []
        invoice_obj = self.pool.get('account.invoice')
        for so in self.browse(cr, uid, ids, context=context):
            invoice_id = invoice_obj.search(cr, uid,[('id','in',so.supp_invoice_ids.ids),('type','=','in_invoice')]) 
            supp_invoice_ids = invoice_obj.browse(cr, uid,invoice_id)
            if so.b2b_invoice:
                inv_ids += [invoice.id for invoice in supp_invoice_ids]
        #choose the view_mode accordingly
        if len(inv_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_supplier_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

    def action_view_invoice(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #compute the number of invoices to display
        inv_ids = []
        invoice_obj = self.pool.get('account.invoice')
        for so in self.browse(cr, uid, ids, context=context):
            invoice_id = invoice_obj.search(cr, uid,[('id','in',so.invoice_ids.ids),('type','=','out_invoice')]) 
            invoice_ids = invoice_obj.browse(cr, uid,invoice_id)
            if so.b2c_invoice:
                inv_ids += [invoice.id for invoice in invoice_ids]
        #choose the view_mode accordingly
        if len(inv_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'


    date_in = fields.Datetime('Date In', default=fields.Datetime.now)
    date_out = fields.Datetime('Date Out', default=fields.Datetime.now)
    product_id = fields.Many2one('product.product', 'Service', domain=[('sale_ok', '=', True)], change_default=True, readonly=True, states={'draft': [('readonly', False)]}, ondelete='restrict')
