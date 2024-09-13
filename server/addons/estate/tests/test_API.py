from odoo.tests import HttpCase
import requests
import json

class TestEstatePropertyTagAPI(HttpCase):

    def setUp(self):
        super(TestEstatePropertyTagAPI, self).setUp()
        self.base_url = "http://localhost:8069"
        self.auth_token = "f632312a-08f0-46d6-aef2-c22614579edf"
        self.session_id = self.authenticate()

    def authenticate(self):
        url = f'{self.base_url}/web/session/authenticate'
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc":"2.0",
            "method":"call",
            "id":1,
            "method":"login",
            "params":{
                "db":"odoo_17",
                "login":"mbisyri44@gmail.com",
                "password":"IPAk1m14"
            },
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
   

    # Tambahkan test case
    def test_get_tag(self):
        url = f'{self.base_url}/estate-property-tags'
        headers = {
            'Authorization': self.auth_token,
            'Cookie': f'session_id={self.session_id}'
        }
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200) 

    
    def test_get_data_by_id(self):
        tag_id = 1
        url = f'{self.base_url}/estate-property-tag/{tag_id}'

        headers = {
            'Authorization': self.auth_token,
            'Cookie': f'session_id={self.session_id}'
        }

        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "id": 1,
            "name": "Red",
            "color": 1
        }

        self.assertEqual(response.json(), expected_response)

