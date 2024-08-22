from ..utilities.authentication_utilities import authenticate
from odoo.http import request, Response
from odoo import http
import json

class EstatePropertyTagController(http.Controller):
    @http.route('/web/session/authenticate_', type='json', auth='none')
    def authenticate_(self, db, login, password):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()
    

    @http.route('/estate-property-tags', auth='public', methods=['GET'])
    @authenticate
    def get_properti_tags(self, **kwargs):
        tags = request.env['estate.property.tag'].search([])

        property_tags = []
        for tag in tags:
            property_tags.append({
                'id': tag.id,
                'name': tag.name,
                'color': tag.color
            })
        
        return Response(json.dumps(property_tags), content_type="application/json")