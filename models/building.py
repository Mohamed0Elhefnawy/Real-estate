from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = 'building'
    _description = 'building record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text(tracking=1)
    active = fields.Boolean(default=True)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_time_next_six_hour')
    
    @api.depends('create_time')
    def _compute_time_next_six_hour(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False












