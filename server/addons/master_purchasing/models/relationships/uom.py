from odoo import fields, models, api

class UnitOfMeasurement(models.Model):
    _name = 'unit.of.measurement'
    _description = 'Unit of Measurement for Master Purchasing'

    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The Unit of measurement name must be unique'
        ),
    ]

    name = fields.Char('Name of Measurement', required=True)
    category = fields.Char(string='Category')
    reference_unit = fields.Char(string='Reference Unit', required=True)
    r_t_r_unit = fields.Float(
        string='Ratio to Reference Unit', default=1 
    )
    symbol = fields.Char(string='Symbol')
    active = fields.Boolean(
        string='Active (being used)',
        default=True
    )
    # bagian yang menghubungkan ke model purchase order
    # purchase_order_ids = fields.One2many(
    #     'purchase.order',
    #     'uom',
    #     string='Properties'
    # )

    @api.constrains
    def _check_ratio(self):
        """
        Ensure the ratio to reference unit is positive.
        """
        for record in self:
            if record.r_t_r_unit <= 0:
                raise ValueError('The ratio to reference unit must be a positive value.')
            
    # display symbol instead of name of measurement 
    # overriding name_get() method
    def name_get(self):
        result = []
        for record in self:
            name = record.symbol if record.symbol else record.name
            result.append((record.id,name))
            
        return result