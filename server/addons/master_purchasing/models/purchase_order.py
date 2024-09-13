from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _description = 'Purchase Order'


    company = fields.Char(string='Company')





