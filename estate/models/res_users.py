from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users"]

    property_ids = fields.One2many("estate_property","user_id",
                                   domain=[("state","not in",['sold','canceled'])])


