from odoo import models


class CustomSaleReportXlsx(models.AbstractModel):
    _name = 'report.custom_sale_report.action_custom_sale_report_wizard'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        sheet = workbook.add_worksheet('Custom Sale Report')
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        simple_bold = workbook.add_format({'bold': True})
        align_center = workbook.add_format({'align': 'left'})
        date_format = workbook.add_format({'align': 'left', 'bold': True, 'bold': True})
        number_format_1 = workbook.add_format({'num_format': '#,###,##0.000', 'align': 'left'})
        number_format_2 = workbook.add_format(
            {'num_format': '#,##0.0', 'bold': True, 'bg_color': 'yellow', 'align': 'left'})
        row = 0
        col = 0

        sheet.merge_range(row, col + 4, row, col + 6, "Sales -- Group By Invoices", bold)
        row += 1
        sheet.merge_range(row, col + 0, row, col + 1, "From: {}".format(report.date_from.strftime('%d/%m/%Y')),
                          date_format)
        row += 1
        sheet.merge_range(row, col + 0, row, col + 1, "To: {}".format(report.date_to.strftime('%d/%m/%Y')), date_format)

        row += 1
        if report.customer_id:
            sheet.merge_range(row, col, row, col + 1, "Customer: {}".format(report.customer_id.name), simple_bold)
        else:
            sheet.merge_range(row, col, row, col + 1, "Salesperson: {}".format(report.salesperson_id.name), simple_bold)

        row = 5
        col = 0

        sheet.set_column('B:B', 24)
        sheet.set_column('C:C', 11)
        sheet.set_column('D:D', 11)
        sheet.set_column('E:E', 11)
        sheet.set_column('F:F', 11)
        sheet.set_column('G:G', 11)
        sheet.set_column('H:H', 11)
        sheet.set_column('I:I', 24)
        sheet.set_column('J:J', 11)
        sheet.set_column('K:K', 11)
        sheet.set_column('L:L', 11)

        results = data.get('result', '').split('\n')

        sheet.write(row, col, 'Cust No', bold)
        sheet.write(row, col + 1, 'Customer', bold)
        sheet.write(row, col + 2, 'Bill no', bold)
        sheet.write(row, col + 3, 'Date', bold)
        sheet.write(row, col + 4, 'Total', bold)
        sheet.write(row, col + 5, 'Invoice disc', bold)
        sheet.write(row, col + 6, 'Item disc', bold)
        sheet.write(row, col + 7, 'Net total', bold)
        sheet.write(row, col + 8, 'Sales Man', bold)
        sheet.write(row, col + 9, 'Cost', bold)
        sheet.write(row, col + 10, 'Profit', bold)
        sheet.write(row, col + 11, 'Profit %', bold)
        row += 1

        subtotal_sum = 0.0
        salesperson_printed = False
        customer_printed = False
        for result in results:
            values = result.split('\t')

            if len(values) >= 8:
                cust_no = values[0].strip()
                salesperson = values[10].strip()
                customer_id = values[1].strip()
                sale_order_name = values[9].strip()
                date = values[5].strip()

                try:
                    invoice_disc = float(values[2].strip())
                except ValueError:
                    invoice_disc = 0.0

                try:
                    quantity = float(values[6].strip())
                except ValueError:
                    quantity = 0.0

                try:
                    net_total = float(values[3].strip())
                except ValueError:
                    net_total = 0.0
                try:
                    cost_value = float(values[7].strip())
                except ValueError:
                    cost_value = 0.0

                try:
                    price_unit = float(values[8].strip())
                except ValueError:
                    price_unit = 0.0

                total_cost = (cost_value * quantity)
                total = (price_unit * quantity)
                profit = (net_total - total_cost)

                if customer_id:
                    if cust_no != 'False':
                        sheet.write(row, col, cust_no, align_center)
                    if cust_no == 'False':
                        sheet.write(row, col, "")

                    sheet.write(row, col + 1, customer_id, align_center)
                    if sale_order_name:
                        sheet.write(row, col + 2, sale_order_name)
                    else:
                        sheet.write(row, col + 2, "")

                    sheet.write(row, col + 3, date)
                    sheet.write(row, col + 4, total, number_format_1)
                    sheet.write(row, col + 5, invoice_disc, number_format_1)
                    sheet.write(row, col + 7, net_total, number_format_1)
                    if total_cost == 0:
                        sheet.write(row, col + 9, "0.0", number_format_1)
                    else:
                        sheet.write(row, col + 9, total_cost, number_format_1)
                    if profit == 0:
                        sheet.write(row, col + 10, "0.0", number_format_1)
                    else:
                        sheet.write(row, col + 10, profit, number_format_1)
                    sheet.write(row, col + 8, salesperson, align_center)

                elif salesperson:
                    if cust_no:
                        sheet.write(row, col, cust_no, align_center)
                    if cust_no == False:
                        sheet.write(row, col, "")

                    sheet.write(row, col + 1, customer_id, align_center)
                    sheet.write(row, col + 2, sale_order_name)
                    sheet.write(row, col + 3, date)
                    sheet.write(row, col + 4, total, number_format_1)
                    sheet.write(row, col + 5, invoice_disc, number_format_1)
                    sheet.write(row, col + 7, net_total, number_format_1)
                    sheet.write(row, col + 8, salesperson, align_center)
                    if total_cost == 0:
                        sheet.write(row, col + 9, "0.0", number_format_1)
                    else:
                        sheet.write(row, col + 9, total_cost, number_format_1)
                    if profit == 0:
                        sheet.write(row, col + 10, "0.0", number_format_1)
                    else:
                        sheet.write(row, col + 10, profit, number_format_1)

                if net_total == 0:
                    profit_percentage = 0
                else:
                    profit_percentage = (profit / net_total) * 100

                sheet.write(row, col + 11, profit_percentage, number_format_1)

                row += 1
