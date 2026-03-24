from email.policy import default

from odoo import fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Tuto"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description',required=True)
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available From',copy=False,
                                    default=fields.Date.today()+timedelta(days=90))
    expected_price = fields.Float('Expected Price',required=True)
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
                   ('sold','Sold'),('cancelled','Cancelled')],
        required=True,
        copy=False,
        default='new'
    )
