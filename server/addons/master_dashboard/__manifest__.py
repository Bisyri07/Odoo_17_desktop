# -*- coding: utf-8 -*-
{
    'name': "master_dashboard",
    'version': '1.0',

    'summary': "Owl dashboard",
    'description': """Owl Custom dashboard using Javascript""",

    'license': 'LGPL-3',
    'author': "Bisyri",
    'sequence':4,

    'website': "https://www.yourcompany.com",
    'category': 'dashboard',
    
    'application': True,
    # 'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sale', 'board'],

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

    # static assets
    # 'assets': {
    #     'web.assets_backend': [
    #         'master_dashboard/static/src/components/**/*.js',
    #         'master_dashboard/static/src/components/**/*.xml',
    #         'master_dashboard/static/src/components/**/*.scss',
    #     ]
    # }
}

