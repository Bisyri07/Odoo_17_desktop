{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base','mail'],
    'author': 'Bisyri',
    'category': 'App',
    'description': 
                    """
                        This is module is used to learn basic technical Odoo 17
                    """,
    'application': True,
    'data': [
        # SECURITY
        'security/ir.model.access.csv',  

        # TEMPLATE (email template)
        'views/templates/email_templates.xml',

        # VIEWS (estate property CRUD form)
        'views/estate_property.xml',   
        # VIEWS (scheduler)
        'views/estate_property_scheduler.xml',
        # VIEWS (property type)
        'views/estate_property_type.xml',
        # VIEWS (property offer)
        'views/estate_property_offer.xml',
        # VIEWS (property tag)
        'views/estate_property_tag.xml',
        # VIEWS (users API)
        'views/users.xml',
        # VIEWS (menu)
        'views/menu.xml', # the order must be like this

        # LOAD DEMO DATA
        'demo/estate_property_tag_demo.xml',

        # LOAD DATA (dummy data) 
        'data/estate.property.csv',

        # REPORTS
        'views/reports/output_pdf/estate_property.xml',

    ],
    'assets': {
        'web.report_assets_common': [
            'estate/static/src/css/ep_report_style.css',
        ],
    },
}