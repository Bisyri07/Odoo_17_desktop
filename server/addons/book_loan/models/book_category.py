from odoo import models, fields

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book Category'
    _rec_name = 'category'

    category = fields.Char(string='Category')
    category_code = fields.Char(string='Code Code', size=10)
