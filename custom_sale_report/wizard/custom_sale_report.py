from odoo import fields, api, models
from odoo.exceptions import ValidationError


class CustomSaleReport(models.TransientModel):
    _name = 'custom.sale.report'
    _description = 'Custom Sale Report'

    customer_id = fields.Many2one('res.partner', string="Customer")
    salesperson_id = fields.Many2one('res.partner', string="SalesPerson",
                                     domain="[('category_id.name', '=', 'Salesperson')]")
    date_from = fields.Date(string="Date from", required=True)
    date_to = fields.Date(string="Date to", default=fields.Datetime.now)
    result = fields.Text(string="result")

    def print_report(self):
        report = self.env.ref('custom_sale_report.report_custom_sale_pdf')
        return report.report_action(self)

    def action_report(self):
        account_move_obj = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]

        if self.customer_id:
            domain.append(('partner_id', '=', self.customer_id.id))

        if self.salesperson_id:
            domain.append(('sales_person_id', '=', self.salesperson_id.id))

        account_moves = account_move_obj.search(domain)

        if not account_moves:
            raise ValidationError('No data to print.')

        result_lines = []

        for move in account_moves:
            result_lines.append(f"\n{move.invoice_date}")

            for move_line in move.invoice_line_ids:
                sale_order_name = move_line.sale_line_ids.order_id.name or ''
                sales_person = move_line.sale_line_ids.order_id.sales_person_id.name or ''

                if self.customer_id:

                    result_line = (
                        f"{move.partner_id.ref}\t"
                        f"{move.partner_id.name}\t"
                        f"{move_line.discount}\t"
                        f"{move_line.price_subtotal}\t"
                        f"{move.partner_id.name}\t"
                        f"{move.invoice_date}\t"
                        f"{move_line.quantity}\t"
                        f"{move_line.product_id.standard_price}\t"
                        f"{move_line.price_unit}\t"
                        f"{sale_order_name}\t"
                        f"{sales_person}\t"

                    )
                    result_lines.append(result_line)
                else:
                    result_line = (
                        f"{move.partner_id.ref}\t"
                        f"{move.partner_id.name}\t"
                        f"{move_line.discount}\t"
                        f"{move_line.price_subtotal}\t"
                        f"{move.partner_id.name}\t"
                        f"{move.invoice_date}\t"
                        f"{move_line.quantity}\t"
                        f"{move_line.product_id.standard_price}\t"
                        f"{move_line.price_unit}\t"
                        f"{sale_order_name}\t"
                        f"{move.sales_person_id.name}\t"

                    )
                    result_lines.append(result_line)

        result_lines = [line + "\tCust No" if line.startswith("\n") else line for line in result_lines]

        print(result_lines)
        self.result = '\n'.join(result_lines)

        action = self.env.ref('custom_sale_report.action_custom_sale_report_wizard').read()[0]
        return action

    def print_custom_sale_report(self):
        self.action_report()
        data = {'result': self.result}
        return self.env.ref('custom_sale_report.action_custom_sale_report_wizard').report_action(self, data=data)

    # def print_pdf_report(self):
    #     self.action_report()
    #     data = {'result': self.result}
    #     return self.env.ref('custom_sale_report.action_report_pdf').report_action(self, data=data)
    def print_pdf_report(self):

        account_move_obj = self.env['account.move']
        domain = [
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]

        if self.customer_id:
            domain.append(('partner_id', '=', self.customer_id.id))

        if self.salesperson_id:
            domain.append(('sales_person_id', '=', self.salesperson_id.id))

        account_moves = account_move_obj.search(domain)
        if not account_moves:
            raise ValidationError('No Data to Print')

        invoices = []
        self_data = [{
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer': self.customer_id.name,
            'salesperosn': self.salesperson_id.name
        }]

        for move in account_moves:
            for move_line in move.invoice_line_ids:
                sale_order_name = move_line.sale_line_ids.order_id.name or ''
                sales_person = move_line.sale_line_ids.order_id.sales_person_id.name or ''
                total_cost = (move_line.product_id.standard_price * move_line.quantity)
                profit = (move_line.price_subtotal - total_cost)
                if profit == 0:
                    profit_perc = 0
                elif profit != 0:
                    profit_perc = (move_line.price_subtotal / profit) * 100

                invoices.append({
                    'cust_no': move.partner_id.ref,
                    'partner_id_name': move.partner_id.name,
                    'disc': move_line.discount,
                    'total': move_line.price_subtotal,
                    'date': move.invoice_date,
                    'qty': move_line.quantity,
                    'std_price': move_line.product_id.standard_price,
                    'price_unit': move_line.price_unit,
                    'name': sale_order_name,
                    'salesperosn': sales_person,
                    'profit': profit,
                    'profit_perc': profit_perc,
                    'total_cost': total_cost
                })
        data = {'result': self.result,
                'inv': invoices,
                'dates': self_data}
        return self.env.ref('custom_sale_report.action_report_pdf').report_action(self, data=data)

    def action_report_cancel(self):
        return
