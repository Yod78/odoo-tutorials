from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )