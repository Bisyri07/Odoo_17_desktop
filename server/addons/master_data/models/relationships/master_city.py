from odoo import fields, models


class MasterCity(models.Model):
    _name ='master.city'
    _description ='Master City'


    name = fields.Char(string='Name of City', 
                       size=50,
                       required=True)
    country_id = fields.Many2one('res.country', 
                                 string='Country', 
                                 )