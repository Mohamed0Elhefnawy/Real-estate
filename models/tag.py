from odoo import models, fields


class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(required=1)



    # validation type  data tier for name
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]


