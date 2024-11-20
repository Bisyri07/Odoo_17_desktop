# -*- coding: utf-8 -*-
# from odoo import http


# class MasterDashboard(http.Controller):
#     @http.route('/master_dashboard/master_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/master_dashboard/master_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('master_dashboard.listing', {
#             'root': '/master_dashboard/master_dashboard',
#             'objects': http.request.env['master_dashboard.master_dashboard'].search([]),
#         })

#     @http.route('/master_dashboard/master_dashboard/objects/<model("master_dashboard.master_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('master_dashboard.object', {
#             'object': obj
#         })

