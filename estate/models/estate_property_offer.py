from odoo import fields, models, api
from datetime import timedelta

from odoo.orm.decorators import readonly


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"


    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner",string="Buyer",required=True)
    property_id = fields.Many2one("estate_property",string="Property",required=True)
    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(string="Deadline",compute="_compute_deadline", inverse="_inverse_deadline",
                                readonly=False)

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            if not offer.create_date:
                date = fields.Date.today()
            else:
                date = offer.create_date

            offer.date_deadline = date+timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if not offer.create_date:
                date = fields.Date.today()
            else:
                date = offer.create_date.date()

            offer.validity = (offer.date_deadline - date).days