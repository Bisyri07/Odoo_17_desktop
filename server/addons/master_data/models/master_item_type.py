from odoo import fields, models, api
from odoo.exceptions import ValidationError

class MasterItemType(models.Model):
    _name='master.item.type'
    _description='Master Item Type'

    item_type = fields.Char(string='Item Type', size=50)
    item_type_code = fields.Char(string='Item Type Code', size=10)


    # python constraints
    @api.constrains('item_type', 'item_type_code')
    def check_item_type(self):
        for record in self:
            if not record.item_type:
                raise ValidationError('Item type cannot be empty!')
            
            if not record.item_type_code:
                raise ValidationError('Item type code cannot be empty!')

    
    # SQL nostraints
    _sql_constraints = [
        ('check_item_type_code',
         'UNIQUE(item_type_code)',
         'Item type code must be unique'
         )
    ] 