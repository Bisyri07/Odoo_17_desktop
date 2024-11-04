# -*- coding: utf-8 -*-
from .token_based_auth import authenticate
from odoo.http import request, Response
from odoo import http
import json


class SalesorderApi(http.Controller):
    # untuk mengakses record melalui autentikasi login akses
    @http.route('/web/session/authenticate_', type='json', auth='none')
    def authenticate_(self, db, login, password):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()


    # untuk mendapatkan record
    @http.route('/master_purchasing', auth='public')
    @authenticate
    def index(self, **kw):
        sales = request.env['sales.order'].search([])
        sales_order_list = []
        for sale in sales:
            sales_order_list.append({
                'id': sale.id,
                'item': sale.item.item,
                'item_code': sale.item_code,
            })
        return Response(json.dumps(sales_order_list), content_type="application/json")

        # another variation
        # sales_order = http.request.env['sales.order'].search([])
        # output = "<h1>Sales order</h1>"
        
        # for sale in sales_order:
        #     output += '<li>' + str(sale['item']) + '</li>'

        # output += '</ul>'
        # return output