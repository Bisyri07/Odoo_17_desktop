from odoo import fields, models

class MasterLocation(models.Model):
    _name = 'master.location'
    _description = 'Master customer'

    loc_name = fields.Char(string='Location Name', 
                           size=50,
                           required=True)
    loc_code = fields.Char(string='Locatio Code', 
                           size=20,
                           required=True)
    description = fields.Text(string='Description')

    warehouse = fields.Char(string='Warehouse', size=50)
    building = fields.Char(string='Building', size=30)
    floor = fields.Char(string='Floor', size=10)
    section = fields.Char(string='section', size=10)
    aisle = fields.Char(string='Aisle', size=10)
    rack = fields.Char(string='Rack', size=20)