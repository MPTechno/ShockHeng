from openerp import api, fields, models
from openerp import workflow
from openerp import SUPERUSER_ID

class purchase_order_wiz(models.TransientModel):
    _name = "purchase.order.wizard"
    _description = "Purchase Order"

    payment_terms = fields.Many2one('custom.payment.term','Payment Terms')

    @api.multi
    def purchase_confirm(self):
        active_ids = self._context.get('active_ids', [])
        purchase = self.env['purchase.order'].browse(active_ids)
        purchase.update({'payment_terms':self.payment_terms.id})
        workflow.trg_validate(SUPERUSER_ID, 'purchase.order', purchase.id, 'purchase_confirm', self._cr)
