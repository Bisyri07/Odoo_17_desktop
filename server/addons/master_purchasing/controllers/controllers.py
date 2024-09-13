# -*- coding: utf-8 -*-
# from odoo import http


# class MasterPurchasing(http.Controller):
#     @http.route('/master_purchasing/master_purchasing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_purchasing/master_purchasing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_purchasing.listing', {
#             'root': '/master_purchasing/master_purchasing',
#             'objects': http.request.env['master_purchasing.master_purchasing'].search([]),
#         })

#     @http.route('/master_purchasing/master_purchasing/objects/<model("master_purchasing.master_purchasing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_purchasing.object', {
#             'object': obj
#         })

