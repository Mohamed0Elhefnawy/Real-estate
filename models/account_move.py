from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('property', string="Property")

    def action_to_execute_any_something(self):
        print(self, "action_to_execute_any_something")






