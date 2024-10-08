from odoo import fields, models, api
from odoo.exceptions import UserError


class MasterCompany(models.Model):
    _name='master.company'
    _description = 'Master Data Company'
    # Specify the field that will be displayed in Many2one relations
    _rec_name = 'company_name'

    company_code = fields.Char(string='Company Code', size=150)
    company_name = fields.Char(string='Company Name', size=50)
    company_level = fields.Integer(string='Company Level')
    address = fields.Text(string='Address')

    parent_code_company = fields.Char(
        string='Parent Code',
        compute='_compute_parent_code'
    )
    """
    a Many2one relationship is allowing the system to store 
    and reference the parent company for each company in the hierarchy
    """ 
    parent_company_id = fields.Many2one(
        comodel_name='master.company',
        string='Parent Company',
        domain="[('company_level', '=', company_level - 1)]"
    )

    @api.depends('company_code', 'company_name', 'company_level', 'parent_company_id')
    def _compute_parent_code(self):
        for record in self:
            # No parent company for level 1
            if record.company_level == 1:
                record.parent_code_company = f"{record.company_code} - {record.company_name}"

            # get parent company code and its name
            elif record.company_level > 1 and record.parent_company_id:

                parent_company = record.parent_company_id
                record.parent_code_company = f"{parent_company.company_code[:3]}-ID - {parent_company.company_name}"

            else:
                record.parent_code_company = False