from openerp import api, fields, models

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    payment_terms_id = fields.Many2one('custom.payment.term','Payment Terms')