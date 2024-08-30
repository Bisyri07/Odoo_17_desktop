from odoo.tests import TransactionCase


class TestEstatePropertyTag(TransactionCase):

    # wajib menggunakan camel case contoh: setUp ✔️ bukan setup ✖️
	def setUp(self):
		super(TestEstatePropertyTag, self).setUp()
		self.estate_property_tag_model = self.env['estate.property.tag']


	def test_create_tag(self):
		tag_data = {
			'name': 'TAG 001',
			'color': 99
		}
		#                             disini create nya
		tag = self.estate_property_tag_model.create(tag_data)
		self.assertEqual(tag.name, 'TAG 001')
		self.assertEqual(tag.color, 99)
		

	def test_read_tag(self):
		new_tag = self.estate_property_tag_model.create({
			'name': 'TAG 002',
			'color': 89
		})
		#       disini read nya     
		tag  = new_tag.read(['name', 'color'])
		self.assertEqual(tag[0]['name'], 'TAG 002')
		self.assertEqual(tag[0]['color'], 89)

	
	def test_update_tag(self):
		tag = self.estate_property_tag_model.create({
			'name': 'TAG 003',
			'color': 79
		})

		tag.write({'color': 70})
		self.assertEqual(tag.color, 70)
