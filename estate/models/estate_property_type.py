from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many("estate_property","property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages.")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )