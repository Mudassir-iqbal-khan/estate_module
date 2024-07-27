# -*- coding: utf-8 -*-
{
    'name': "Real Estate Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        This is a test module of Real-Estate Management!
  Written for the Odoo Quickstart Tutorial.
    """,

    'author': "Mudassir iqbal",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Category',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
        'views/property_type_views.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/css/custom.css',
        ],
    },
  # 'installable': True,
  # 'auto_install': False,
  # 'application': False,
}
