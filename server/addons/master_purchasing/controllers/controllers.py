# -*- coding: utf-8 -*-
from odoo.tools import html_escape, html_sanitize
from .token_based_auth import authenticate
from odoo.http import request, Response
from markupsafe import Markup
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


class PythonTemplate(http.Controller):
    @http.route('/python_template', type='http', auth='public', website=True)
    def display_qweb(self, **kw):

        def some_function():
            return "returning string from function"
        
        some_model = http.request.env['sales.order'].sudo().search([])

        data = {
            'string': 'QWEB Tutorials',
            'integer': 1000,
            'some_float': 12.54,
            'boolean': True,
            'some_list': [1,2,3,4,5],
            'some_dict': {'any_key':'any_value'},
            'some_function': some_function(),
            'model': some_model,
            'html': '<h3>This is an HTML value!</h3>',
            'html_escape': '<h3>This is an HTML value!</h3> %s' % html_escape('Added by attacker <script>alert("Fix your page or I will hack it!s")</script>'),
            'html_sanitize': '<h3>This is an HTML value!</h3> %s' % html_sanitize('Added by attacker <script>alert("Fix your page or I will hack it!s")</script>'),
            'markup': Markup('<h3>This is an HTML value!</h3> %s') % 'Added by attacker <script>alert("Fix your page or I will hack it!s")</script>',
        }

        return request.render('master_purchasing.PythonTemplate', data)
    

    @http.route('/python_template/form', type="json", auth="public")
    def qweb_form(self, **kw):
        print(kw)

        return {"status" : 1}
    

    @http.route('/python_template/owl', type="http", auth="public")
    def qweb_tutorial_owl(self, **kw):
        return http.request.render("master_purchasing.my_owl_app")