# -*- coding: utf-8 -*-
# from odoo import http


# class BookLoan(http.Controller):
#     @http.route('/book_loan/book_loan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/book_loan/book_loan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('book_loan.listing', {
#             'root': '/book_loan/book_loan',
#             'objects': http.request.env['book_loan.book_loan'].search([]),
#         })

#     @http.route('/book_loan/book_loan/objects/<model("book_loan.book_loan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('book_loan.object', {
#             'object': obj
#         })

