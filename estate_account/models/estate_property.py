from odoo import models, Command
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]


    def sold_property(self)->bool:
        commission = 6 * self.selling_price / 100
        invoice_info = [
            {'partner_id':self.partner_id.id,
             'move_type':'out_invoice',
             'journal_id':1,
             'invoice_line_ids':[
                Command.create({
                    "name": "Commission",
                    "quantity": 1,
                    "price_unit":commission
                }),
                 Command.create({
                     "name": "Administrative fees",
                     "quantity": 1,
                     "price_unit": 100.00
                 }),
               ],
             }
        ]

        account_move = self.env["account.move"].create(invoice_info)
        return super().sold_property()
