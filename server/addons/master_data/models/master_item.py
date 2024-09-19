from odoo import fields, models

class MasterItem(models.Model):
    _name='master.item'
    _description='Master Item'

    item = fields.Char(string='Item Name')
    item_code = fields.Char(string="Item Code")
    