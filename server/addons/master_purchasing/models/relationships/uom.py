from odoo import fields, models, api

class UnitOfMeasurement(models.Model):
    _name = 'unit.of.measurement'
    _description = 'Unit of Measurement for Master Purchasing'
    _rec_name = 'symbol'
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
        string='Ratio to Reference Unit', 
        default=1,
        digits=(12, 6) 
    )
    symbol = fields.Char(string='Symbol')
    active = fields.Boolean(
        string='Active (being used)',
        default=True
        )


    @api.constrains
    def _check_ratio(self):
        """
        Ensure the ratio to reference unit is positive.
        """
        for record in self:
            if record.r_t_r_unit <= 0:
                raise ValueError('The ratio to reference unit must be a positive value.')
            
    # overriding name_get() method, display symbol instead of name of measurement 
    def name_get(self):
        result = []
        for record in self:
            uom_symbol = record.uom.symbol if record.uom else ''
            # format sesuai kebutuhan
            name = f'{record.po_no} - {uom_symbol}'
            result.append((record.id,name))
            
        return result
