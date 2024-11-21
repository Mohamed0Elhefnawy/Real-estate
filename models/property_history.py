from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'property history'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    next_state = fields.Char()
    reason = fields.Char()
    line_ids = fields.One2many('property.line.history', 'property_history_id')


class PropertyLineHistory(models.Model):
    _name = 'property.line.history'

    area = fields.Float()
    property_history_id = fields.Many2one('property.history')
    description = fields.Char()














