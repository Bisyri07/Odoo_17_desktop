from odoo import fields, models, api


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _rec_name = 'name'


    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    published_date = fields.Date(string='Tanggal Terbit')
    category =  fields.Many2one(comodel_name='book.category', string='Kategori')
    total_copies = fields.Integer(string='Jumlah Salinan', required=True)
    available_copies = fields.Integer(string='Salinan yang Tersedia', compute='_compute_available_copies')
    amount = fields.Integer(string='Jumlah yang dipinjam', store=True)


    # Computed field total (ppn + subtotal)
    @api.depends('amount')
    def _compute_available_copies(self):
        for a in self:
            a.available_copies = a.total_copies - a.amount

