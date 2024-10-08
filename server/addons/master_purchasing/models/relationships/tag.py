from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PurchasingTag(models.Model):
    _name='purchasing.tag'
    _description='Purchasing Tag Data'
    _order='color'

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique')
    ]

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer("Color Index")
    tag_type = fields.Selection(
        [
            ('priority','Priority'),
            ('urgency','Urgency'),
            ('category','Category'),
            ('status','Status'),
            ('vendor_type','Vendor Type'),
            ('shipment_type','Shipment Type'),
            ('customs','Customs'),
            ('payment_status','Payment Status'),
            ('inspection','Inspection'),
        ],
        string='Tag Type',
        required=True,
        help='Specify the type of tag'
    )

    # python constraints
    @api.constrains('color')
    def check_color(self):
        for record in self:
            if record.color > 100:
                raise ValidationError('color index must be lower than 100')
            