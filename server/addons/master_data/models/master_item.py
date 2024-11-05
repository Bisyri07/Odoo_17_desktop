from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class MasterItem(models.Model):
    _name='master.item'
    _description='Master Item'
    _rec_name='item'


    item = fields.Char(string='Item Name')
    name = fields.Char(related='item', store=True, readonly=True)
    item_code = fields.Char(string="Item Code", size=50)
    company_id = fields.Many2one(comodel_name='master.company', string='Company')
    company_code = fields.Char(related='company_id.company_code', 
                               string='Company code',
                               store=True)
    location_id = fields.Many2many(comodel_name='master.location', string='Item Location')
    location_code = fields.Char(compute='_compute_location_code', 
                                string='Location Code',
                                store=True)
    item_type = fields.Many2one(comodel_name='master.item.type', string='Item Type')
    item_type_code = fields.Char(related='item_type.item_type_code', 
                                 string='Item Type Code',
                                 store=True)
    quantity = fields.Integer(string='Qty')
    # company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    
    # change currency to currency_id
    currency_id = fields.Many2one(comodel_name='res.currency', 
                                  string='Currency',
                                  default=lambda self: self.env.company.currency_id) 
    acq_date = fields.Date(string='Acquisition Date / Tanggal Pembelian', default=fields.Datetime.now)
    acq_period = fields.Char(string='Acquisition Period', size=6)
    acq_cost = fields.Monetary(string='Acquisition Cost / Nilai Pembelian', currency_field='currency_id')
    year_of_useful = fields.Integer(string='Year of Useful Life')
    month_of_useful = fields.Integer(string='Month of Useful Life')
    salvage_value = fields.Monetary(string='End of Useful Value (Salvage Value)', currency_field='currency_id')
    order_id = fields.Integer(string='Order Id', readonly=True)
    opening_accum_dep = fields.Monetary(string='Opening Accumulated Depreciation', currency_field='currency_id')
    sales_amount = fields.Monetary(string='Sales Amount', currency_field='currency_id')
    item_cost = fields.Monetary(string='Item Cost / Harga per Barang', currency_field='currency_id')
    
    # computed fields
    monthly_dep = fields.Monetary(string='Monthly Depreciation', 
                                  currency_field='currency_id',
                                  compute='_compute_monthly_dep',
                                  store=True)
    monthly_dep_pct = fields.Float(string='Monthly Depreciation Percentage (%)',
                                   compute='_compute_monthly_dep_pct',
                                   store=True)
    annual_dep = fields.Monetary(string='Annual Depreciation', 
                                 currency_field='currency_id',
                                 compute='_compute_annual_dep',
                                 store=True)
    annual_dep_pct = fields.Float(string='Annual Depreciation Percentage (%)',
                                  compute='_compute_annual_dep_pct',
                                  store=True)
    

    # SQL constraints
    _sql_constraints = [
        (
            'check_price',
            'CHECK(item_cost > 0)',
            'Item Cost / Harga per Barang must be greater than zero!'
        ),
        (
            'check_quantity', 
            'CHECK(quantity > 0)', 
            'Quantity must be greater than zero!'
        ),
        (
            'check_acq_cost',
            'CHECK(acq_cost > 0)',
            'Acquisition cost must be greater than zero!'
        ),
    ]

    """Python constraints"""
    @api.constrains('currency_id')
    def _checking_currency_id(self):
        for record in self:
            if not record.currency_id:
                raise ValidationError('Currency field cannot be empty')


    """computed field"""
    # acquisition cost
    @api.depends('quantity', 'item_cost')
    def _compute_acq_cost(self):
        for record in self:
            if record.quantity and record.item_cost:
                record.acq_cost = record.quantity * record.item_cost
            else:
                record.acq_cost = 0


    # annual depreciation
    @api.depends('acq_cost', 'salvage_value', 'year_of_useful')
    def _compute_annual_dep(self):
        for record in self:
            if record.year_of_useful and record.year_of_useful > 0:
                record.annual_dep = (record.acq_cost - record.salvage_value) / record.year_of_useful
            else:
                record.annual_dep = 0    

    # annual depreciation percentage
    @api.depends('acq_cost', 'annual_dep')
    def _compute_annual_dep_pct(self):
        for record in self:
            if record.acq_cost and record.acq_cost > 0:
                record.annual_dep_pct = (record.annual_dep / record.acq_cost) * 100
            else:
                record.annual_dep_pct = 0

    # monthly depreciation
    @api.depends('annual_dep')
    def _compute_monthly_dep(self):
        for record in self:
            if record.annual_dep and record.annual_dep > 0:
                record.monthly_dep = record.annual_dep / 12 
            else:
                record.monthly_dep = 0

    # monthly depreciation percentage
    @api.depends('acq_cost', 'monthly_dep')
    def _compute_monthly_dep_pct(self):
        for record in self:
            if record.acq_cost and record.acq_cost > 0:
                record.monthly_dep_pct = (record.monthly_dep / record.acq_cost) * 100 
            else:
                record.monthly_dep_pct = 0

    # item code 
    @api.depends('location_id')
    def _compute_location_code(self):
        for record in self:
            if record.location_id:
                if len(record.location_id) == 1:
                    # location_id should have one location_code
                    record.location_code = record.location_id.loc_code                   
                else:
                    location_codes = [loc.loc_code for loc in record.location_id]
                    record.location_code = "_".join(location_codes)
            else:
                record.location_code = ''

    """order_id sequence"""
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if not record.get('order_id'):
                record['order_id'] = self.env['ir.sequence'].next_by_code('order.id.sequence')
        
        return super(MasterItem, self).create(vals_list)        


    status = fields.Selection(
        selection=[
            ('input','Input'),
            ('confirmed','Confirmed'),
            ('canceled','Canceled'),
    ],
    required=True,
    string = 'Status',
    default='input'
    )

    """action button"""
    # confirm button
    def action_confirmed(self):
        if 'canceled' in self.mapped('status'):
            raise UserError('Canceled Item cannot be confirmed')
        
        self.write({'status':'confirmed'})
    
    # cancel button
    def action_canceled(self):
        if 'confirmed' in self.mapped('status'):
            raise UserError('Confirmed Item cannot be canceled')
        
        self.write({'status':'canceled'})
    