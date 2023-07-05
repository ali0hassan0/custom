# -*- coding: utf-8 -*-
{
    'name': "Custom Sale Report",

    'summary': """
        This module add a menu custom sale report under reporting menu of sale module which opens a wizard
        with customoer salesperson and date range filter out their respective invoices""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'sale',
    'version': '0.1',

    'depends': ['base', 'sale',],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/cusotm_sale_report.xml',
        'reports/cusotm_sale_report.xml',
        'reports/template_custom_sale_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'sequence': -67,
    'price': '1.0',
    'currency': 'USD',
    'images': 'static/description/main.jpeg',
    'category':'sale',
    'maintainer': 'Ali Hassan',
}
