from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]


    def sold_property(self)->bool:
        return super().sold_property()