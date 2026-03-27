from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"

    name = fields.Char('Type', required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )