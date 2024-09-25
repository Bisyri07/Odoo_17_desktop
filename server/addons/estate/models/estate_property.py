from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    # order the list view by date_availability
    _order = "date_availability desc"

    # sql constraints for validation error.
    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'The name must be unique.'
        ),
        (
            'check_percentage',
            'CHECK(facades >= 0 AND facades <= 10)',
            'The number input should be between 0 and 10.'
        ),      
    ]

    # python constraints for validation error.
    @api.constrains('selling_price', 'expected_price')
    def _checking_price(self):
        for record in self:
            if record.selling_price <= 0:
                raise  ValidationError("The selling price must be positive value.")
            if record.expected_price <= record.selling_price:
                raise ValidationError("The expected value must higher than selling price")

    # computed field using python decorator
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for a in self:
            a.total_area = a.living_area + a.garden_area

    # python decorator for condition
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False
            

    name = fields.Char(string="Name", required=True)
    description = fields.Text(default="You can change this description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string='Date Availability', default=fields.Datetime.now)
    expected_price = fields.Float()
    selling_price = fields.Float(default=100000000)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [
            ("N", "North"), ("S", "South"), ("E", "East"), ("W", "West")
        ],
        string = "Garden Orientation",
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

    user_id = fields.Many2one("res.users", 
                              string="salesman", 
                              default=lambda self: self.env.user)
    
    buyer_id = fields.Many2one("res.partner",
                               string="buyer", 
                               readonly=True,
                               copy=False)
    
    total_area = fields.Integer(readonly=True,
                                compute="_compute_total_area")
    
    # states (status of a record within a workflow)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("ready", "Ready"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new"
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # condition for action button
    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled property cannot be sold.")
        return self.write({"state": "sold"})
    
    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})


    # Overriding existing odoo CRUD method
    @api.model_create_multi
    def create(self, vals):
        if vals.get("selling_price") and vals.get("date_availability"):
            vals["state"] = "ready"

        return super().create(vals)
    
    # delete the data
    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled status can be deleted")
        
        return super().unlink()

    
    # scheduler
    def update_status_scheduler(self):
        if not self.date_availability:
            self.env["estate.property"].search([('date_availability', '=', False)]).write({"state":"canceled"}) 


    # sending an email
    def action_send_email(self):
        template = self.env.ref("estate.simple_example_email_template")
        email_values = {
            "email_to": "mbisyri33@gmail.com",
            "email_cc": False,
            "auto_delete": True,
            "recipient_ids": [],
            "partner_ids": [],
            "scheduled_date": False,
            "email_from": "mbisyri22@gmail.com",
        }

        template.send_mail(
            self.id,
            email_values = email_values,
            force_send = True,
        )









