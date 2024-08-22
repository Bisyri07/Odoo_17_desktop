from odoo import models, fields, api
import uuid

class resUsers(models.Model):
    _inherit = "res.users"

    auth_token = fields.Char(string="Authentication token", copy=False)

    @api.model
    def create(self, vals):
        vals['auth_token'] = self.auth_token_generator()
        return super(resUsers, self).create(vals)

    def generate_auth_token(self):
        for user in self:
            user.auth_token = self.auth_token_generator()
        return True
    
    def auth_token_generator(self):
        return str(uuid.uuid4())
    

