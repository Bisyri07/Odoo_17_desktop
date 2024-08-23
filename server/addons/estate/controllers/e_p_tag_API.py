from ..utilities.authentication_utilities import authenticate
from odoo.http import request, Response
from odoo import http
import json

class EstatePropertyTagController(http.Controller):
    # untuk mengakses record melalui autentikasi login akses
    @http.route('/web/session/authenticate_', type='json', auth='none')
    def authenticate_(self, db, login, password):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()


    # untuk mendapatkan semua records di dalam estate property tag
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


    # untuk mendapatkan (GET) 1 record berdasarkan tag id nya
    @http.route('/estate-property-tag/<int:tag_id>', auth='public', methods=['GET'])
    @authenticate
    def get_properti_tag_id(self, tag_id, **kwargs):
        try:
            tag = request.env['estate.property.tag'].browse(tag_id)  
            response_data = {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color
            }

            return Response(json.dumps(response_data), content_type="application/json")
        
        except Exception as e:
            return Response(json.dumps({
                'error': 'something went wrong',
                'error detail': str(e)
            }), status=400)
        
        
    # untuk update (POST) record 
    @http.route('/estate-property-tag', auth='public', methods=['post'], csrf=False)
    @authenticate
    def create_tag(self, **kwargs):
        try:
            request_data = json.loads(request.httprequest.data.decode("utf-8"))
            name = request_data.get('name')
            color = int(request_data.get('color'))

            if not all([name, color]):
                return Response("Bad Request: name and color are required", status=400)

            tag_exist = request.env['estate.property.tag'].search([('name', '=', name)])
            
            if tag_exist:
                return Response(f"Tag with this name ({name}) is already exist!", status=400)
            
            tag = request.env['estate.property.tag'].create({
				'name': name,
				'color': color
			})

            response = json.dumps({'id': tag.id, 'name': name, 'color': color})
            return Response(response, content_type="application/json")

        except Exception as e:
            return Response(f"There is error occured: {str(e)}", status=500)
        
