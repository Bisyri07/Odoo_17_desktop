from odoo import fields, models, api
from odoo.exceptions import ValidationError

class MasterLocation(models.Model):
    _name = 'master.location'
    _description = 'Master customer'
    # Specify the field that will be displayed in Many2one relations
    _rec_name = 'loc_name'

    # important
    loc_name = fields.Char(string='Location Name', 
                           size=50,
                           required=True)
    loc_code = fields.Char(string='Location Code', 
                           size=20,
                           required=True)

    # additional
    warehouse = fields.Char(string='Warehouse', size=50)
    building = fields.Char(string='Building', size=30)
    floor = fields.Char(string='Floor', size=10)
    section = fields.Char(string='section', size=10)
    aisle = fields.Char(string='Aisle', size=10)
    rack = fields.Char(string='Rack', size=20)
    color = fields.Integer("Color Index")
    description = fields.Text(string='Description')

    # python constraints
    @api.constrains('color')
    def check_color(self):
        for record in self:
            if record.color > 100:
                raise ValidationError('color index must be lower than 100')