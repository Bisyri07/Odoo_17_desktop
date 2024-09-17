# -*- coding: utf-8 -*-
{
    'name': "Master Purchasing",
    'version':'1.0',
    'summary': "purchasing data center",

    'description': """
    This module contains all the common menus related to purchasing like:
    1. purchase order, purchase receiving, sales and delivery order
    """,

    'author': "Bisyri",
    'website': "https://github.com/Bisyri07/Odoo_17_desktop",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchasing',
    'version': '0.1',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sequences/po_sequence.xml',
        'views/relationships/uom.xml',
        'views/purchase_order.xml',
        'views/main_menu.xml',

        # scheduler
        'views/schedulers/purchase_order_scheduler.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

