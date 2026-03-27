from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"



    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False,
        readonly=False
    )
    partner_id = fields.Many2one("res.partner",string="Buyer",required=True)
    property_id = fields.Many2one("estate_property",string="Property",required=True)
    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(string="Deadline",compute="_compute_deadline", inverse="_inverse_deadline",
                                readonly=False)

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            _logger.info("length offer, offer=%s", len(self))
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


    def accept_offer(self)->bool:
        for offer in self.property_id.offer_ids:
            if offer.status == "accepted":
                raise UserError("You can accept only one offer")

        if self.status == "refused":
            raise UserError("You cannot accept a refused offer")

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        return True

    def refuse_offer(self)->bool:
        if self.status in ("accepted", "refused"):
            raise UserError("You cannot refuse this offer")

        self.status = "refused"
        return True