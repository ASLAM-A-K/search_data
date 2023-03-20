{
    'name': "Search Data",
    'version': "16.0.1.0.0'",
    'category': "Administration",
    'description': """Search Data""",
    'summary': """Search Data module brings a user to search any data from the 
                  odoo database""",
    'depends': [
        'base'
    ],
    'data': [
        'views/search_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
