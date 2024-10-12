from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class MasterCustomer(models.Model):
    _name = 'master.customer'
    _description = 'Master Customer'
    _rec_name = 'customer'

    customer = fields.Char(string='Customer Name', required=True)
    customer_id = fields.Char(string='Customer Id', readonly=True, default='New')
    phone_num = fields.Char(string='Phone No.')
    city_id = fields.Many2one(comodel_name='master.city', string='City')
    address = fields.Char(string='Address', size=200)
    billing_address = fields.Char(string='Billing Address', size=200)
    shipping_address = fields.Char(string='Shipping Address', size=200)
    contact = fields.Char(string='Contact Person', size=150)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    credit_limit = fields.Monetary(currency_field='currency_id', string='Credit Limit')
    term = fields.Integer(string='Term')
    payment = fields.Char(string='Payment', size=100)
    fax = fields.Char(string='Fax')
    acc_code = fields.Char(string='Acc Code', size=10)
    npwp = fields.Char(string='NPWP', size=40)
    lang = fields.Many2one('res.lang', string='Language')
    status = fields.Selection(
        selection=[
            ('active','Active'),
            ('inactive','Inactive')
        ],
        string='Status',
        required=True
    )
        

    # create sequence of customer_id
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if not record.get('customer_id') or record['customer_id'] == _('New'):
                record['customer_id'] = self.env['ir.sequence'].next_by_code('customer.id.sequence') or _('New')
            
        return super(MasterCustomer, self).create(vals_list)

