# -*- coding: utf-8 -*-
{
    'name': "Master Purchasing",
    'version':'1.0',
    'summary': "purchasing data center",
    'sequence':2,

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
    'depends': ['base','mail', 'portal'],

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
        'web.assets_frontend': [
            'master_purchasing/static/src/js/*',
        ],
        'my_owl_app.assets':[
            # Bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap_backend'),

            # required for fa icons
            'web/static/src/libs/fontawesome/css/font-awesome.css',

            # include base files from framework
            ('include', 'web._assets_core'),

            # remove some files that we do not use to create a minimal bundle
            # ('remove', 'web/static/src/core/**/*'),
            # ('remove', 'web/static/lib/luxon/luxon.js'),
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',

            # custom assets
            'master_purchasing/static/src/components/*'

        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

