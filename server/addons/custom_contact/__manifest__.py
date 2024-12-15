{
	"name": "Custom Contact",
    "summary": "Custom Contact tutorial",
	"description":"""
		In this tutorial, you will learn how the Odoo Web Client architecture works. 
		A diagram will be shown to demonstrate the frontend and backend part of Odoo.
	""",
    "version":"1.0",
    'sequence':6,
    'author':"Bisyri",
    'license':"LGPL-3",
    'website':"https://github.com/Bisyri07/Odoo_17_desktop/tree/owl_javascript_framework",
    "application":True,
    
	"data": {
        # security access
        "security/ir.model.access.csv",
	
		# views
        "views/contact_view.xml",
	},
}