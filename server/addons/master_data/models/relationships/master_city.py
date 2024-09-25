from odoo import fields, models
# from odoo.exceptions import ValidationError


class MasterCity(models.Model):
    _name ='master.city'
    _description ='Master City'


    name = fields.Char(string='Name of City', 
                       size=50,
                       required=True)
    country_id = fields.Many2one('res.country', 
                                 string='Country', 
                                 )
    
    _sql_constraints = [
        (
            'unique_city_name',
            'UNIQUE(name)',
            'The city name must be unique'
        )
    ]