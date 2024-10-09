from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class DeliveryOrder(models.Model):
    _name = 'delivery.order'
    _description = 'Delivery Order'

    # from sales order
    so_number = fields.Many2one(comodel_name='sales.order', string='SO Number')
    do_no = fields.Char(string='Delivery Number', readonly=True, copy=False, default='New')
    company = fields.Many2one(comodel_name='master.company', string='Company', required=True) 
    company_code = fields.Char(related='company.company_code', string='Company Code', store=True)
    create_date = fields.Date(string='Create Date', default=fields.Datetime.now)
    doc_date = fields.Date(string='Document Date')
    from_ = fields.Many2one(comodel_name='master.location', string='From')
    to_ = fields.Many2one(comodel_name='master.company', string='To')
    address = fields.Text(related='so_number.address', string='Alamat', store=True)
    item_sales = fields.Many2one(related='so_number.item', string='Product')
    qty_req = fields.Integer(related='so_number.qty', string='Quantity (Request)', store=True)
    qty_reserved = fields.Integer(related='item_master.quantity', string='Quantity (Reserved)', store=True) 
    qty_done = fields.Integer(string='Quantity (Done)') 
    # from master item
    item_master = fields.Many2one(comodel_name='master.item', string='item_id')

    operating_type = fields.Selection(
        selection=[
            ('penjualan','Penjualan'),
            ('promosi/bonus','Promosi / Bonus'),
            ('sampel penjualan','Sampel Penjualan'),
            ('retain sample','Retain Sample'),
            ('konsiyansi','Konsiyansi'),
            ('retur penjualan','Retur Penjualan'),
            ('write off','Write Off'),
            ('lain-lain','Lain-lain'),
        ]
    )

    status = fields.Selection(
        selection=[
            ('waiting','Waiting'),
            ('ready','Ready'),
            ('done','Done'),
        ],
        string='Status',
        default='waiting',
        required=True
    )


    """sequence"""
    # delivery order sequence
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if not record.get('do_no') or record['do_no'] == _('New'):
                current_year = datetime.now().strftime('%y')
                company = self.env['master.company'].browse(record['company'])
                company_code = company.company_code or 'UNKNOWN'
                sequence = self.env['ir.sequence'].next_by_code('delivery.order.sequence') or _('New')
                record['do_no'] = f"{current_year}-{company_code}-{sequence}"

        return super(DeliveryOrder, self).create(vals_list)


    """Onchange"""
    # The onchange method triggers a warning when the user selects "Penjualan" as the operating_type
    @api.onchange('operating_type')
    def _onchange_operating_type(self):
        if self.operating_type == 'penjualan':
            self.so_number = False
            return {
                'warning': {
                    'title': "SO Number Required",
                    'message': "Please fill in the SO number for 'Penjualan' operating type."
                }         
            }
        
    # raise validation error while SO number is not filled
    @api.constrains('operating_type', 'so_number')
    def _check_so_number(self):
        for a in self:
            if a.operating_type == 'penjualan' and not a.so_number:
                raise ValidationError("SO Number is required for 'Penjualan' operating type.")
            
    # check item
    @api.onchange('so_number')
    def _onchange_so_number(self):
        """
        Automatically match item_sales with item_master and ensure qty_req and qty_reserved
        refer to the same item.
        """
        if self.so_number:
            self.item_master = self.item_sales
            if self.item_master and self.qty_req > self.qty_reserved:
                raise ValidationError('The requested quantity exceeds the reserved quantity for this item.')


    """Action button"""
    def action_ready(self):
        self.write({'status':'ready'})


    def action_done(self):
        for a in self:
            if a.qty_done < a.qty_req:
                raise ValidationError('Cannot set status to Done. Quantity done is less than requested.')
            
            self.write({'status':'done'})

        # rainbowman
        return {
            'effect': 
                    {
                        'fadeout': 'slow',
                        'message': 'your delivery order has been done!',
                        'type': 'rainbow_man',
                    }
        }


    """line model"""
    delivery_order_lines = fields.One2many(
        # Name of the new model
        comodel_name='delivery.order.line',
        # Field in the line model that links back to delivery.order
        inverse_name='delivery_order_id',
        string='Delivery Order Lines'
    )

# model for delivery order lines
class DeliveryOrderLine(models.Model):
    _name = 'delivery.order.line'
    _description = 'Delivery Order Line'


    delivery_order_id = fields.Many2one(
        comodel_name='delivery.order',
        string='Delivery Order Id'
        )

    item_master = fields.Many2one(comodel_name='master.item', string='Item Master')
    item_sales = fields.Many2one(related='delivery_order_id.item_sales', string='Product')
    description = fields.Text(related='delivery_order_id.so_number.description', string='Description', store=True)
    uom = fields.Many2one(comodel_name='master.uom', string='UoM')
    qty_req = fields.Integer(related='delivery_order_id.so_number.qty', string='Quantity (Request)', store=True)
    qty_reserved = fields.Integer(related='item_master.quantity', string='Quantity (Reserved)', store=True) 
    qty_done = fields.Integer(string='Quantity (Done)') 
    
