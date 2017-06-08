# -*- coding: utf-8 -*-
from openerp import api, fields, models

class stock_picking_wave(models.Model):
    _inherit = 'stock.picking.wave'

#     @api.multi
#     def print_picking(self):
#         pickings = self.mapped('picking_ids')
#         if not pickings:
#             raise UserError(_('Nothing to print.'))
#         return self.env["report"].with_context(active_ids=pickings.ids, active_model='stock.picking').\
#             get_action([], 'picking_wave_modifier_template.custom_picking_wave_report_template')
            
            
    
    
    def print_picking(self, cr, uid, ids, context=None):
        '''
        This function print the report for all picking_ids associated to the picking wave
        '''
        context = dict(context or {})
        picking_ids = []
        for wave in self.browse(cr, uid, ids, context=context):
            picking_ids += [picking.id for picking in wave.picking_ids]
        if not picking_ids:
            raise osv.except_osv(_('Error!'), _('Nothing to print.'))
        context['active_ids'] = picking_ids
        context['active_model'] = 'stock.picking'
        return self.pool.get("report").get_action(cr, uid, [], 'picking_wave_modifier_template.custom_picking_wave_report_template', context=context)