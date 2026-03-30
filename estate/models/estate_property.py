
from odoo import fields, models, api
from datetime import timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Tuto"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description',required=True)
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From',copy=False,
                                    default=fields.Date.today()+timedelta(days=90))
    expected_price = fields.Float('Expected Price',required=True)
    best_price = fields.Float(compute="_get_best_price")
    selling_price = fields.Float('Selling Price',required=False, readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', required=True, default=2)
    living_area = fields.Integer('Living area (sqm)', required=True)
    facades = fields.Integer('Facades',required=True)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden',default=False)
    garden_area = fields.Integer('Garden area (sqm)',required=False)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),('east','East'),('west','West')],
        help="Garden Orientation")
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),
                   ('sold','Sold'),('canceled','Canceled')],
        required=True,
        copy=False,
        default='new',
        readonly=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users",string="Salesman",default=lambda self: self.env.uid)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id","Offer")
    total_area = fields.Integer(compute="_compute_total_area", readonly=True)


    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for p in self:
            p.total_area = p.living_area + p.garden_area

    @api.depends("offer_ids.price")
    def _get_best_price(self):
        for p in self:
            p.best_price = max(p.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""


    def sold_property(self)->bool:

        if self.state == "canceled":
            raise UserError("A canceled property cannot be sold")

        self.state = "sold"
        return True

    def cancel_property(self)->bool:
        if self.state == "sold":
            raise UserError("A sold property cannot be canceled")

        self.state = "canceled"
        return True

    @api.constrains("selling_price","expected_price")
    def _check_prices(self):
        for p in self:
            min_amount = p.expected_price * 90 / 100
            if float_compare(p.selling_price,min_amount,2) == -1 and p.offer_ids.status == "accepted":
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")


    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'A property selling price must be strictly positive'
    )
