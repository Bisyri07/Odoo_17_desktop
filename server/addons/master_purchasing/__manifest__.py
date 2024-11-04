# -*- coding: utf-8 -*-
{
    'name': "Master Purchasing",
    'version':'1.0',
    'summary': "purchasing data center",

    'description': """
    This module contains all the common menus related to purchasing like:
    purchase order, purchase receiving, sales and delivery order
    """,

    'author': "Bisyri",
    'website': "https://github.com/Bisyri07/Odoo_17_desktop",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchasing',
    'version': '1.0',
    'application': True,
    # 'installable': True,
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        # access
        'security/ir.model.access.csv',

        # email template for purchase order
        'views/template/po_email_template.xml',  
        # qweb template
        'views/template/py_template.xml',

        # wizard
        'views/wizards/canceled_SO.xml',
        
        # sequence
        'views/sequences/po_sequence.xml',
        'views/sequences/so_sequence.xml',
        'views/sequences/do_sequence.xml',
        
        # relations
        'views/relationships/tag.xml',
        
        # menus
        'views/purchase_order.xml',
        'views/sales_order.xml',
        'views/delivery_order.xml',
        'views/delivery_order_line.xml',    
        'views/main_menu.xml',

        # report
        'views/reports/sales_order_report.xml',

        # scheduler
        'views/schedulers/purchase_order_scheduler.xml',

    ],

    'assets': {
        'web.report_assets_common': [
            'master_purchasing/static/src/*'
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

