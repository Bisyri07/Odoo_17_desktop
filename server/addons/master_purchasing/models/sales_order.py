from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class SalesOrder(models.Model):
    _name = 'sales.order'
    _description = 'Sales Order'
    

    item = fields.Many2one(comodel_name='master.item', string="Item Name")
    item_code = fields.Char(related='item.item_code', string="Item Code", store=True)
    qty = fields.Integer(string="Quantity", required=True)
    so_no = fields.Char(string='SO No', readonly=True, default='New')
    so_date = fields.Date(string='SO Date', required=True, default=fields.Datetime.now)
    input_date = fields.Date(string='Input Date', default=fields.Datetime.now)
    customer = fields.Many2one(comodel_name='master.customer', string='Customer')
    customer_code = fields.Char(related='customer.customer_id', string='Customer Id', store=True)
    contact_person = fields.Char(string='Contact Person')
    term_of_payment = fields.Char(string='Term of Payment (days)')
    currency = fields.Many2one('res.currency', string='Currency')  # Currency field
    currency_rate = fields.Float(string='Currency Rate')
    unit_price = fields.Monetary(related='item.unit_price', string='Unit Price', currency_field='currency')
    description = fields.Text(string='Description')
    company_name = fields.Many2one(comodel_name='master.company', string='Company Name', required=True)
    discount_pct = fields.Float(string='Discount (%)', readonly=True)
    input_by = fields.Many2one(comodel_name='res.users', string='Input By')
    confirm_by = fields.Char(string='Confirm By')
    description = fields.Text(string='Description')
    uom = fields.Many2one(comodel_name='master.uom', string='UoM')
    so_email = fields.Char(size=25, string='SO E-mail', default='youremail@gmail.com')
    tag_id = fields.Many2many(comodel_name='purchasing.tag')
    unit_weight = fields.Float(string='Unit Weight')
    ppn_pct = fields.Float(string='PPN percentage (%)') 
    status = fields.Selection(
        selection=[
            ('draft', 'Draft'), 
            ('confirmed', 'Confirmed'), 
            ('canceled', 'Canceled')
        ],
        required = True,
        string = 'Status',
        default='draft'
    )

    # SQL Constraints
    _sql_constraints = [
        ('check_qty_positive', 'CHECK(qty >= 0)', 'The quantity must be positive!'),
        ('check_unit_price_positive', 'CHECK(unit_price > 0)', 'The price must be greater than zero!')
    ]
    
    """computed fields"""
    subtotal = fields.Monetary(string='Subtotal',
                               currency_field='currency',
                               compute='_compute_subtotal',
                               store=True)
    discount = fields.Monetary(string='Discount',
                               currency_field='currency',
                               compute='_compute_discount',
                               store=True)
    ppn = fields.Monetary(string='PPN',
                               currency_field='currency',
                               compute='_compute_ppn',
                               store=True)
    total = fields.Monetary(string='Total',
                               currency_field='currency',
                               compute='_compute_total',
                               store=True)

    # subtotal 
    @api.depends('unit_price', 'qty')
    def _compute_subtotal (self):
        for a in self:
            if a.qty:
                a.subtotal = a.unit_price * a.qty
            else:
                a.subtotal = 0

    # discount
    @api.depends('subtotal', 'discount_pct')
    def _compute_discount(self):
        for a in self:
            if a.subtotal >= 100000000:
                a.discount_pct = 15
                a.discount = a.subtotal * (a.discount_pct/100)
                a.subtotal = a.subtotal - a.discount
            else:
                a.discount = 0
                a.discount_pct = 0

    # ppn
    @api.depends('ppn_pct', 'subtotal')
    def _compute_ppn(self):
        for a in self:
            if a.ppn_pct:
                a.ppn = a.subtotal * (a.ppn_pct/100)
            else:
                a.ppn = 0.0

    # total 
    @api.depends('subtotal', 'ppn')
    def _compute_total (self):
        for a in self:
            a.total = a.subtotal + a.ppn

    # sequence for Sales Order
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if not record.get('so_no') or record['so_no'] == _('New'):
                # Extract the last two digits of the current year
                current_year = datetime.now().strftime('%y')  # e.g., '24' for 2024
                # Get the item code
                item_code = self.env['master.item'].browse(record['item']).item_code
                # Generate the sequence number
                sequence = self.env['ir.sequence'].next_by_code('sales.order.sequence') or _('New')
                # Combine year, item_code and sequence into SO number
                record['so_no'] = f"{current_year}-{item_code}-{sequence}"
            
        return super(SalesOrder, self).create(vals_list)
    

    """action button"""
    def action_confirmed(self):
        if 'canceled' in self.mapped('status'):
            raise ValidationError('canceled sales order cannot be confirmed')

        self.write({'status': 'confirmed'})

        # rainbowman
        return {
            'effect': 
                    {
                        'fadeout': 'slow',
                        'message': 'your sales order has been confirmed!',
                        'type': 'rainbow_man',
                    }
        }
    
    def action_canceled(self):
        if 'confirmed' in self.mapped('status'):
            raise ValidationError('confirmed sales order cannot be canceled')
        
        self.write({'status','canceled'})
