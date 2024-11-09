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
    available_copies = fields.Integer(
        string='Salinan yang Tersedia', compute='_compute_available_copies', store=True
    )
    book_loan_id = fields.One2many(comodel_name='book.loan',inverse_name='book_id', string='Loans')

    @api.depends('total_copies', 'book_loan_id.amount', 'book_loan_id.state')
    def _compute_available_copies(self):
        for record in self:
            loaned_copies = sum(
                loan.amount  for loan in record.book_loan_id if loan.state == 'dipinjam'
            )
            record.available_copies = record.total_copies - loaned_copies

