from odoo import models, fields, api
from datetime import timedelta

class BookLoan(models.Model):
    _name = 'book.loan'
    _description = 'Book loan'
    _rec_name = 'name'

    name = fields.Char(string='Nama Peminjam')
    contact_name = fields.Char(string='Kontak Peminjam')
    book_id = fields.Many2one(comodel_name='library.book', string='Nama Buku', required=True)
    loan_date = fields.Date(string='Tanggal Peminjaman', default=fields.Date.today)
    loan_term = fields.Integer(string='jangka waktu pinjaman', required=True)
    return_date = fields.Date(string='Tanggal Pengembalian', compute='_compute_return_date')
    amount = fields.Integer(string='Jumlah yang dipinjam')
    state = fields.Selection(
        selection=[
            ('dipinjam','dipinjam'),
            ('dikembalikan','Dikembalikan'),
            ('hilang','Hilang'),
        ],
        string='Status',
        default='dipinjam',
        required=True
    )

    """Computed fields"""
    @api.depends('loan_date', 'loan_term')
    def _compute_return_date(self):
        for record in self:
            record.return_date = record.loan_date + timedelta(days=record.loan_term)


    """action button"""
    def action_return(self):
        self.state = 'dikembalikan'

    def action_borrow(self):
        self.state = 'dipinjam'

    def action_lost(self):
        self.state = 'hilang'
