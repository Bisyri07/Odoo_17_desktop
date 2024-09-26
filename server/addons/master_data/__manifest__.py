{
    'name': "Master Data",
    'version':'1.0',
    'summary': "Master data center",

    'description': """
    This module contains all the common menus related to Master data like:
    Item, Item Category, Supplier, Customer, User etc.
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
        
        # sequences
        'views/sequences/customer_id.xml',
        'views/sequences/supplier_id.xml',

        # relationships
        'views/relationships/city.xml',

        # views
        'views/customer.xml',
        'views/company.xml',
        'views/item_type.xml',
        'views/item.xml',
        'views/supplier.xml',    
        'views/main_menu.xml',

        # scheduler       

        # data seeding
        'data/master.city.csv',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}