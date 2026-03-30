from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages.")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

