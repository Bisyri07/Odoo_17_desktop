{
    'name': "Master Data",
    'version':'1.0',
    'summary': "Master data center",

    'description': """
    This module contains all the common menus related to Master data like:
    Item, Item Category, Vendor, Customer, User etc.
    """,

    'author': "Bisyri",
    'website': "https://github.com/Bisyri07/Odoo_17_desktop",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Master Data',
    'version': '1.0',
    'application': True,
    # 'installable': True,
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # 'views/templates/po_email_template.xml',  
        
        'views/item.xml',    
        'views/main_menu.xml',

        # scheduler
        # 'views/schedulers/purchase_order_scheduler.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}