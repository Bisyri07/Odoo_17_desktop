from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MasterSupplier(models.Model):
    _name = 'master.supplier'
    _description = 'Master Supplier'
    _rec_name = 'supplier'

    supplier = fields.Char(string='Supplier')
    supplier_code = fields.Char(string='Supplier Code', readonly=True, default='New')
    contact = fields.Char(string='Contact Person')
    phone = fields.Char(string='Phone number', size=25)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    active_condition = fields.Selection(
        selection=[
            ('yes', 'Yes'),
            ('no', 'No')
        ],
        string='Active',
        required=True
    )

    # python constraints
    @api.constrains('supplier')
    def _check_supplier(self):
        for record in self:
            if not record.supplier:
                raise ValidationError('Supplier name cannot be empty')
            
    
    # create sequence for supplier_id
    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:       
            if not record.get('supplier_id') or record['supplier_id'] == _('New'):
                record['supplier_id'] = self.env['ir.sequence'].next_by_code('supplier.id.sequence') or _('New')

        return super(MasterSupplier, self).create(vals_list)
    