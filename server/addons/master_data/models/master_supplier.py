from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MasterSupplier(models.Model):
    _name = 'master.supplier'
    _description = 'Master Supplier'

    supplier = fields.Char(string='Vendor/Supplier')
    supplier_id = fields.Char(string='Supplier Id', readonly=True, default='New')
    contact = fields.Char(string='Contact Person')
    phone = fields.Char(string='Phone number', size=25)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    activity = fields.Selection(
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
    def create(self, vals):        
        if not vals.get('supplier_id') or vals['supplier_id'] == _('New'):
            vals['supplier_id'] = self.env['ir.sequence'].next_by_code('supplier.id.sequence') or _('New')

        return super(MasterSupplier, self).create(vals)
    
