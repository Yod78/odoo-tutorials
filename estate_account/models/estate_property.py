from odoo import models, Command
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]


    def sold_property(self)->bool:
        invoice_info = [
            {'partner_id':self.partner_id.id,
             'move_type':'out_invoice',
             'journal_id':1,
             'invoice_line_ids':[
                Command.create({
                    "name": "Commission",
                    "quantity": 1,
                    "price_unit":200.00
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

    # def _create_invoices(self, grouped=False, final=False, date=None):
    #     """
    #     Create the invoice associated to the SO.
    #     :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
    #                     (partner_invoice_id, currency)
    #     :param final: if True, refunds will be generated if necessary
    #     :returns: list of created invoices
    #     """
    #     if not self.env['account.move'].check_access_rights('create', False):
    #         try:
    #             self.check_access_rights('write')
    #             self.check_access_rule('write')
    #         except AccessError:
    #             return self.env['account.move']
    #
    #     precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #
    #     # 1) Create invoices.
    #     invoice_vals_list = []
    #     invoice_item_sequence = 0
    #     for order in self:
    #         order = order.with_company(order.company_id)
    #         current_section_vals = None
    #         down_payments = order.env['sale.order.line']
    #
    #         # Invoice values.
    #         invoice_vals = order._prepare_invoice()
    #
    #         # Invoice line values (keep only necessary sections).
    #         invoice_lines_vals = []
    #         for line in order.order_line:
    #             if line.display_type == 'line_section':
    #                 current_section_vals = line._prepare_invoice_line(sequence=invoice_item_sequence + 1)
    #                 continue
    #             if line.display_type != 'line_note' and float_is_zero(line.qty_to_invoice, precision_digits=precision):
    #                 continue
    #             if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final) or line.display_type == 'line_note':
    #                 if line.is_downpayment:
    #                     down_payments += line
    #                     continue
    #                 if current_section_vals:
    #                     invoice_item_sequence += 1
    #                     invoice_lines_vals.append(current_section_vals)
    #                     current_section_vals = None
    #                 invoice_item_sequence += 1
    #                 prepared_line = line._prepare_invoice_line(sequence=invoice_item_sequence)
    #                 invoice_lines_vals.append(prepared_line)
    #
    #         # If down payments are present in SO, group them under common section
    #         if down_payments:
    #             invoice_item_sequence += 1
    #             down_payments_section = order._prepare_down_payment_section_line(sequence=invoice_item_sequence)
    #             invoice_lines_vals.append(down_payments_section)
    #             for down_payment in down_payments:
    #                 invoice_item_sequence += 1
    #                 invoice_down_payment_vals = down_payment._prepare_invoice_line(sequence=invoice_item_sequence)
    #                 invoice_lines_vals.append(invoice_down_payment_vals)
    #
    #         if not any(new_line['display_type'] is False for new_line in invoice_lines_vals):
    #             raise self._nothing_to_invoice_error()
    #
    #         invoice_vals['invoice_line_ids'] = [(0, 0, invoice_line_id) for invoice_line_id in invoice_lines_vals]
    #
    #         invoice_vals_list.append(invoice_vals)
    #
    #     if not invoice_vals_list:
    #         raise self._nothing_to_invoice_error()
    #
    #     # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
    #     if not grouped:
    #         new_invoice_vals_list = []
    #         invoice_grouping_keys = self._get_invoice_grouping_keys()
    #         for grouping_keys, invoices in groupby(invoice_vals_list,
    #                                                key=lambda x: [x.get(grouping_key) for grouping_key in
    #                                                               invoice_grouping_keys]):
    #             origins = set()
    #             payment_refs = set()
    #             refs = set()
    #             ref_invoice_vals = None
    #             for invoice_vals in invoices:
    #                 if not ref_invoice_vals:
    #                     ref_invoice_vals = invoice_vals
    #                 else:
    #                     ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
    #                 origins.add(invoice_vals['invoice_origin'])
    #                 payment_refs.add(invoice_vals['payment_reference'])
    #                 refs.add(invoice_vals['ref'])
    #             ref_invoice_vals.update({
    #                 'ref': ', '.join(refs)[:2000],
    #                 'invoice_origin': ', '.join(origins),
    #                 'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
    #             })
    #             new_invoice_vals_list.append(ref_invoice_vals)
    #         invoice_vals_list = new_invoice_vals_list
    #
    #     # 3) Create invoices.
    #     # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
    #     # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
    #     moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
    #     # 4) Some moves might actually be refunds: convert them if the total amount is negative
    #     # We do this after the moves have been created since we need taxes, etc. to know if the total
    #     # is actually negative or not
    #     if final:
    #         moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
    #     for move in moves:
    #         move.message_post_with_view('mail.message_origin_link',
    #                                     values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
    #                                     subtype_id=self.env.ref('mail.mt_note').id
    #                                     )
    #     return moves