# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrder(http.Controller):
#     @http.route('/purchase_order/purchase_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order/purchase_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order.listing', {
#             'root': '/purchase_order/purchase_order',
#             'objects': http.request.env['purchase_order.purchase_order'].search([]),
#         })

#     @http.route('/purchase_order/purchase_order/objects/<model("purchase_order.purchase_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order.object', {
#             'object': obj
#         })

