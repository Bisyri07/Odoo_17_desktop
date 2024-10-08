from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _description = 'Purchase Order'


    item = fields.Many2one(comodel_name='master.item', string="Item Name")
    item_code = fields.Char(related='item.item_code', string="Item Code", store=True)
    qty = fields.Integer(string="Quantity")
    po_no = fields.Char(string='PO Number', readonly=True, copy=False, default='New')
    po_date = fields.Date(string='PO Date', required=True, default=fields.Datetime.now)
    supplier = fields.Many2one(comodel_name='master.supplier',string='Supplier')
    supplier_code = fields.Char(related='supplier.supplier_code', string='Supplier Code')
    contact_person = fields.Char(string='Contact Person')
    term_of_payment = fields.Char(string='Term of Payment (days)')
    expired_date = fields.Date(string='Expired Date')
    currency = fields.Many2one('res.currency', string='Currency')  # Currency field
    currency_rate = fields.Float(string='Currency Rate')
    description = fields.Text(string='Description')
    company_name = fields.Many2one(comodel_name='master.company', string='Company Name')
    discount_pct = fields.Float(string='Discount (%)', readonly=True)
    ppn_pct = fields.Float(string='PPN (%)')
    pph_pct = fields.Float(string='PPH (%)')
    pph = fields.Monetary(string='PPH', currency_field='currency')
    item_cost = fields.Monetary(related='item.item_cost', string='Unit Price', currency_field='currency', store=True)
    input_by = fields.Many2one(comodel_name='res.users', string='Input By')
    confirm_by = fields.Char(string='Confirm By')
    date_input = fields.Date(string='Date Input', default=fields.Datetime.now)
    posted_by = fields.Char(string='Posted By')
    date_posted = fields.Date(string='Date Posted')
    unit_weight = fields.Float(string='Unit Weight')
    uom = fields.Many2one(comodel_name='master.uom', string='UoM')
    email_po = fields.Char(string='PO E-mail', default='youremail@gmail.com')
    state = fields.Selection(
        selection=[
            ('input', 'Input'), 
            ('confirmed', 'Confirm'), 
            ('canceled', 'Canceled')
        ], 
        required=True,
        string='Status', 
        default='input'
    )
    tag_ids = fields.Many2many('purchasing.tag', string='Tags')
    

    # function for action button
    def action_confirmed(self):
        if 'canceled' in self.mapped('state'):
            raise UserError('Canceled Purchase Order cannot be confirmed')
        
        self.write({'state':'confirmed'})

        # Trigger the rainbow man animation
        return {
                'effect': 
                    {
                        'fadeout': 'slow',
                        'message': 'your purchase order has been confirmed!',
                        'type': 'rainbow_man',
                    }
               }
    
    def action_canceled(self):
        if 'confirmed' in self.mapped('state'):
            raise UserError('Confirmed Purchase Order cannot be canceled')
        self.write({'state':'canceled'})

    # SQL Constraints
    _sql_constraints = [
        ('check_qty_positive', 'CHECK(qty >= 0)', 'The quantity must be positive!'),
        ('check_item_cost_positive', 'CHECK(item_cost > 0)', 'The price must be greater than zero!')
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
    discount = fields.Monetary(string='Discount', 
                               currency_field='currency',
                               compute='_compute_discount', store=True) 


    # Computed field subtotal (item_cost * ppn_pct / 100)
    @api.depends('item_cost', 'qty')
    def _compute_subtotal_biaya(self):
        for a in self:
            if a.qty:
                a.subtotal = a.item_cost * a.qty 
            else:
                a.subtotal = 0.0

    # Computed field discount
    @api.depends('subtotal', 'discount', 'discount_pct')
    def _compute_discount(self):
        for a in self:
            if a.subtotal >= 100000000:
                a.discount_pct = 15
                a.discount = a.subtotal * (a.discount_pct/100)
                a.subtotal = a.subtotal - a.discount
            else:
                a.discount = 0.0
                a.discount_pct = 0.0


    # Computed field PPN (subtotal * ppn_pct)
    @api.depends('ppn_pct', 'subtotal', 'ppn')
    def _compute_ppn(self):
        for a in self:
            if a.ppn_pct:
                a.ppn = a.subtotal * (a.ppn_pct/100)
            else:
                a.ppn = 0.0


    # Computed field total (ppn + subtotal)
    @api.depends('subtotal', 'ppn')
    def _compute_total_biaya(self):
        for a in self:
            a.total = a.subtotal + a.ppn


    # Override the create method to generate a PO number
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if not record.get('po_no') or record['po_no'] == _('New'):
                record['po_no'] = self.env['ir.sequence'].next_by_code('purchase.order.sequence') or _('New')
        
        return super(PurchaseOrder, self).create(vals_list) 
    

    # Override the delete method
    def unlink(self):
        if not set(self.mapped('state')) <= {'canceled', 'input'}:
            raise UserError('Only input and canceled purchase order status can be deleted')
    
        return super().unlink()
    

    # Scheduler
    def po_scheduler(self):
        today = fields.Date.today()

        # calculate po_date minus today
        expired_po = self.search([
            ('expired_date', '<', today),
            ('state', '!=', 'canceled')
        ])

        # change po status to canceled because expired
        for po in expired_po:
            po.write({'state':'canceled'})


    # Send an email
    def action_send_email(self):
        # make sure the email field is not empty
        if not self.email_po:
            raise UserError('Please set en email address for the purchase order')

        # prepare email template
        template_id = self.env.ref('master_purchasing.mail_template_purchase_order').id
        email_template = self.env['mail.template'].browse(template_id)

        # send an email
        email_template.send_mail(self.id, force_send=True) 

