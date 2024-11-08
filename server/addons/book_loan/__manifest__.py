# -*- coding: utf-8 -*-
{
    'name': "Peminjaman Buku",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Module ini dibuat untuk melakukan kegiatan peminjaman buku di perpustakaan
    """,

    'author': "Bisyri",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Book',
    'version': '1.0',
    'application':True,
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        # security access
        'security/ir.model.access.csv',

        # qweb template
        # 'views/templates.xml',
        
        # menus
        'views/book_category_data.xml',
        'views/book.xml',
        'views/book_loan.xml',
        'views/main_menu.xml',

        # data seeding
        'data/book.category.csv',
        'data/library.book.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}

