from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft')
    reason = fields.Char()

    def confirm_action_change_state(self):
        if self.property_id.state != 'closed':
            raise ValidationError('invalid change state')
        else:
            self.property_id.state = self.state
            self.property_id.create_property_history('close', self.state, self.reason)


