from odoo.tests import TransactionCase

class estatePropertyTagTest(TransactionCase):

    def setup(self):
        super(estatePropertyTagTest).setUp()
        self.estate_property_tag_model = self.env['estate.property.tag']
    