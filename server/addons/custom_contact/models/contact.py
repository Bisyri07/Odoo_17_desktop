from odoo import fields, models


class CustomContact (models.Model):
    _name = "custom.contact"
    _description = "Custom Contact"


    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")  