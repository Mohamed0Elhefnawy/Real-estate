from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import json


class Property(models.Model):
    _name = 'property'
    _description = 'property record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, default='New', size=50, translate=True)
    ref = fields.Char(default='New', readonly=1)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_date_selling = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('solid', 'Solid'),
        ('closed', 'Closed'),
    ], default='draft')

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside compute diff")
            rec.diff = (rec.expected_price or 0.0) - (rec.selling_price or 0.0)

    # this functions for calculate diff between
    # onchange return sudo record and depend return real record in onchange relational كانها مش شيفاها
    @api.onchange('expected_price')
    def _onchange_compute_diff(self):
        for rec in self:
            # print(rec)
            # print("inside onchange_compute_diff")
            return {
                'warning': {'title': 'warning', 'message': 'negative value', 'type': 'notification'}
            }
    owner_id = fields.Many2one('owner')  # all data from table owner
    tag_ids = fields.Many2many('tag')
    phone_owner = fields.Char(related='owner_id.phone', readonly=0)   # only phone owner from table owner
    address_owner = fields.Char(related='owner_id.address', readonly=0)  # only address owner from table owner

    # validation type  data tier for name
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    # for lines
    line_ids = fields.One2many('property.line', 'property_id')

    # this func check_value data type is float_greater_zero
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms')

    # overwriting inheritance
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        print("inside create method")
        return res

    # this functions for workflow in ui
    def action_draft(self):
        for rec in self:
            rec.create_property_history(rec.state, 'draft', reason=None)
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_property_history(rec.state, 'pending', reason=None)
            rec.state = 'pending'

    def action_solid(self):
        for rec in self:
            rec.create_property_history(rec.state, 'solid', reason=None)
            rec.state = 'solid'

    def action_closed(self):
        for rec in self:
            rec.create_property_history(rec.state, 'closed', reason=None)
            rec.state = 'closed'

    # automated action
    def check_expected_date_selling(self):
        print("check_expected_date_selling")
        property_ids = self.search([])
        print(property_ids)
        for rec in property_ids:
            if rec.expected_date_selling and rec.expected_date_selling < fields.Date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    # fun to action server for change state
    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action')
        action['context'] = {'default_property_id': self.id}

        return action

    # title sequence
    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    # property state history
    def create_property_history(self, old_state, next_state, reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'next_state': next_state,
                'reason': reason,
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids]
            })

    # fun related on button action in view to print result from domain
    def action(self):
        print(self.env['property'].search(['|', ('name', 'like', 'Property'), ('postcode', '=', '455')]))

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    # integration with another app --> end point display all properties with ids
    def integration_end_point(self):
        try:
            payload = dict()
            response = requests.get('http://localhost:8069/v1/properties', data=payload)
            res = json.loads(response.content)
            if response.status_code == 200:
                print(res)
                print('successful')
                print(response.content)
                ids = [item['data']['id'] for item in res if 'data' in item and 'id' in item['data']]
                print(f"IDs: {ids}")

            else:
                print("invalid")
        except Exception as error:
            raise ValidationError(str(error))

    def property_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/v1/property/excel/report/{self.env.context.get("active_ids")}',
            'target': 'new'
        }





    # @api.model
    # # after refresh
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("inside search  method")
    #     return res
    #
    # # after updating on record
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write method")
    #     return res
    #
    # # after delete record
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside delete method")
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    property_id = fields.Many2one('property')
    description = fields.Char()

