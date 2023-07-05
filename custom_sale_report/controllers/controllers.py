# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSaleReport(http.Controller):
#     @http.route('/custom_sale_report/custom_sale_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_report/custom_sale_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_report.listing', {
#             'root': '/custom_sale_report/custom_sale_report',
#             'objects': http.request.env['custom_sale_report.custom_sale_report'].search([]),
#         })

#     @http.route('/custom_sale_report/custom_sale_report/objects/<model("custom_sale_report.custom_sale_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_report.object', {
#             'object': obj
#         })
