from odoo import models, fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1, default='New', size=15)
    phone = fields.Char(required=1)
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')

    # validation type  data tier for name
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]


