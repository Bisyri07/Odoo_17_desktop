from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _description = 'Purchase Order'


    item_code = fields.Char(string="Item Code")
    item = fields.Char(string="Item")
    qty = fields.Integer(string="Quantity")
    po_no = fields.Char(string='PO Number', readonly=True, copy=False, default='New')
    po_date = fields.Datetime(string='PO Date', required=True, default=fields.Datetime.now)
    supplier_code = fields.Char(string='Supplier Code')
    supplier = fields.Char(string='Supplier')
    contact_person = fields.Char(string='Contact Person')
    term_of_payment = fields.Char(string='Term of Payment (days)')
    expired_date = fields.Date(string='Expired Date')
    currency = fields.Many2one('res.currency', string='Currency')  # Currency field
    currency_rate = fields.Float(string='Currency Rate')
    description = fields.Text(string='Description')
    company_name = fields.Char(string='Company Name')
    discount_pct = fields.Float(string='Discount (%)')
    discount = fields.Monetary(string='Discount', currency_field='currency')  # Correct reference to currency
    ppn_pct = fields.Float(string='PPN (%)')
    pph_pct = fields.Float(string='PPH (%)')
    pph = fields.Monetary(string='PPH', currency_field='currency')
    unit_price = fields.Monetary(string='Unit Price', currency_field='currency')
    input_by = fields.Char(string='Input By')
    confirm_by = fields.Char(string='Confirm By')
    date_input = fields.Datetime(string='Date Input', default=fields.Datetime.now)
    posted_by = fields.Char(string='Posted By')
    date_posted = fields.Datetime(string='Date Posted')
    unit_weight = fields.Float(string='Amount of unit')
    uom = fields.Selection(
        [
            ('kg', 'Kilogram'),
            ('g', 'gram'),
            ('liter', 'Liter'),
            ('ml', 'Mililiter'),
        ], 
        string='Unit of Measurement',
        default='kg'
    )

    status = fields.Selection(
        selection=[
            ('input', 'Input'), 
            ('confirmed', 'Confirm'), 
            ('canceled', 'Canceled')
        ], 
        required=True,
        string='Status', 
        default='input'
    )

    # function for action button
    def action_confirmed(self):
        if 'canceled' in self.mapped('status'):
            raise UserError('Confirmed Purchase Order cannot be canceled')
        return self.write({'status':'confirmed'})
    
    def action_canceled(self):
        if 'confirmed' in self.mapped('status'):
            raise UserError('Canceled Purchase Order cannot be confirm')
        return self.write({'status':'canceled'})

    # SQL Constraints
    _sql_constraints = [
        ('check_qty_positive', 'CHECK(qty >= 0)', 'The quantity must be positive!'),
        ('check_unit_price_positive', 'CHECK(unit_price > 0)', 'The price must be greater than zero!')
    ]
    

    # Field untuk menyimpan subtotal, ppn dan total
    subtotal = fields.Monetary(string='Subtotal', 
                               currency_field='currency', 
                               compute='_compute_subtotal_biaya', store=True)
    total = fields.Monetary(string='Total', 
                            currency_field='currency', 
                            compute='_compute_total_biaya', store=True)
    ppn = fields.Monetary(string='PPN',
                          currency_field='currency',
                          compute='_compute_ppn', store=True)


    # Computed field subtotal (unit_price * ppn_pct / 100)
    @api.depends('unit_price', 'qty')
    def _compute_subtotal_biaya(self):
        for a in self:
            if a.qty:
                a.subtotal = a.unit_price * a.qty 
            else:
                a.subtotal = 0.0

    # Computed field PPN (subtotal * ppn_pct)
    @api.depends('ppn_pct', 'subtotal', 'ppn')
    def _compute_ppn(self):
        for a in self:
            if a.ppn_pct:
                a.ppn = a.subtotal * (a.ppn_pct/100)
            else:
                a.ppn = 0.0

    # Computed field total (unit_price + subtotal)
    @api.depends('unit_price', 'ppn')
    def _compute_total_biaya(self):
        for a in self:
            a.total = a.subtotal + a.ppn


    # Override the create method to generate a PO number
    @api.model
    def create(self, vals):
        if vals.get('po_no', 'New') == 'New':
            # Generate PO number from sequence
            vals['po_no'] = self.env['ir.sequence'].next_by_code('purchase.order.sequence')
        
        return super(PurchaseOrder, self).create(vals) 
    
    # Override the delete method
    def unlink(self):
        if not set(self.mapped('status')) <= {'canceled', 'input'}:
            raise UserError('Only input and canceled purchase order status can be deleted')
    
        return super().unlink()
