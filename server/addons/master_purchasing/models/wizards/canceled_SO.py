from odoo import fields, models, api

class CancelSoWizard(models.Model):
    _name = 'cancel.sales.order.wizard'
    _description = 'Cancel Sales Order Wizard'

    cancel_reason = fields.Char(string='Cancellation Reason', required=True)
    responsible_user = fields.Many2one(comodel_name='res.users', 
                                       string='Responsible User', 
                                       required=True,
                                       default=lambda self: self.env.user)
    
    def action_cancel_sales_order(self):
        # Retrieve the active sales order record
        sales_order = self.env['sales.order'].browse(self.env.context.get('active_id'))

        # Update the reason for cancellation
        sales_order.write({
            'status': 'canceled',
            'description': f"Canceled by {self.responsible_user.name}: {self.cancel_reason}",
        })
        return {'type': 'ir.actions.act_window_close'}
       