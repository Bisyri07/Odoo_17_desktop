# -*- coding: utf-8 -*-
{
    'name': "purchase_order",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    This module is used to make Purchase Order process
    """,

    'author': "Bisyri",
    'website': "https://github.com/Bisyri07",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Application',
    'version': '0.1',
    
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

