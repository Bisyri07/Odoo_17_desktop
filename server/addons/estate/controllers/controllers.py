from ..utilities.authentication_utilities import authenticate
from odoo import http
import requests
import json

class EstateProperty(http.Controller):
    @http.route('/estate_property_menu', auth='public', methods=['GET', 'POST'])
    def estateMenu(self, **kw):
        return "This Is Estate Property Menu Page!"
    
    @http.route('/user_login', auth='user')  # disini bakal disuruh login dulu
    def login(self, **kw):
        return 'welcome to odoo'

    @http.route('/test_property', auth='public')
    @authenticate
    def test_property(self, **kw):
        api_url = "https://api.bridgedataoutput.com/api/v2/OData/test/Property?access_token=6baca547742c6f96a6ff71b138424f21"

        response = requests.get(api_url)

        return json.dumps(response.json())











