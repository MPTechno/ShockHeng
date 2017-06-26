# -*- coding: utf-8 -*-
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class VehicleInsuranceClaims(models.Model):
    _name = "vehicle.insurance.claims"
    _inherit = ['mail.thread']
    _description = "Vehicle Insurance Claims"
    _rec_name = "number"
    _order = "number desc, id desc"

    @api.one
    @api.depends('insurance_line.price_subtotal')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.insurance_line)
        self.amount_total = self.amount_untaxed
        
    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    @api.model
    def _default_company(self):
        return self.env.user.company_id.id

    number = fields.Char('Number')
    comment = fields.Text('Additional Information')
    state = fields.Selection([
            ('draft','Draft'),
            ('confirmed','Confirmed'),
            ('approve','Approved'),
            ('refuse','Refuse')],'Status',default='draft')
    insurance_date = fields.Date(string='Insurance Date',
            help="Keep empty to use the current date")
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True,
        default=_default_currency, track_visibility='always')
    partner_id = fields.Many2one('res.partner', string='Customer', change_default=True,
             required=True, track_visibility='always')
    insurance_line = fields.One2many('vehicle.insurance.claims.line', 'insurance_id', 
             string='Invoice Lines', copy=False)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
             default=_default_company, track_visibility='always')
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
             store=True, readonly=True, compute='_compute_amount')

    _sql_constraints = [
        ('number_uniq', 'unique(number)',
            'Insurance Number must be unique per Company!'),
    ]

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].\
            next_by_code('insurance.claims') or '/'
        return super(VehicleInsuranceClaims, self).create(vals)

    @api.multi
    def action_insurence_confirm(self):
        """
        This method is used to change the state 
        to confirmed of the Vehicle Insurance
        --------------------------------------------
        @param self : object pointer
        """
        for on in self:
            on.state = 'confirmed'
    
    @api.multi
    def action_insurence_refuse(self):
        """
        This method is used to change the state 
        to  of the Vehicle Insurance
        --------------------------------------------
        @param self : object pointer
        """
        for on in self:
            on.state = 'refuse'

    @api.multi
    def action_insurence_approve(self):
        """
        This method is used to change the state 
        to approved of the Vehicle Insurance
        and sets the approver who approves it
        --------------------------------------------
        @param self : object pointer
        """
        for on in self:
            on.state = 'approve'

    @api.multi
    def action_insurence_draft(self):
        """
        This method is used to change the state 
        to approved of the Vehicle Insurance
        and sets the approver who approves it
        --------------------------------------------
        @param self : object pointer
        """
        for on in self:
            on.state = 'draft'


class VehicleInsuranceClaimsLine(models.Model):
    _name = "vehicle.insurance.claims.line"
    _description = "Vehicle Insurance Claims Line"
    _order = "insurance_id,sequence,id"

    @api.one
    @api.depends('price_unit', 'discount', 'quantity',
        'product_id', 'insurance_id.partner_id', 'insurance_id.currency_id', 'insurance_id.company_id',
        'insurance_id.insurance_date')
    def _compute_price(self):
        currency = self.insurance_id and self.insurance_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        self.price_subtotal  = self.quantity * price

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            name = self.vehicle_id.model_id.brand_id.name \
                   + '/' + \
                   self.vehicle_id.model_id.modelname \
                   + '/' + \
                   self.vehicle_id.license_plate
            self.name = name

    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(default=10,
        help="Gives the sequence of this line when displaying the Insurance.")
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicles',
        ondelete='cascade', index=True)
    insurance_id = fields.Many2one('vehicle.insurance.claims', string='Insurance Reference',
        ondelete='cascade', index=True)
    uom_id = fields.Many2one('product.uom', string='Unit of Measure',
        ondelete='set null', index=True, oldname='uos_id')
    product_id = fields.Many2one('product.product', string='Product',
        ondelete='restrict', index=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float(string='Amount',
        store=True, readonly=True, compute='_compute_price')
    quantity = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        required=True, default=1)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'),
        default=0.0)
    company_id = fields.Many2one('res.company', string='Company',
        related='insurance_id.company_id', store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
        related='insurance_id.partner_id', store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', related='insurance_id.currency_id', store=True)
