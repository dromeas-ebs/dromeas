# -*- coding: utf-8 -*-
{
    'name': "ebs_dromeas_api",

    'summary': """
        Manufacturing API for Dromeas""",

    'description': """
        Manufacturing API for Dromeas
    """,

    'author': "jaafar khansa",
    'website': "http://www.ever-bs.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
         # 'security/ir.model.access.csv',
        'wizards/message_wiz_view.xml',
        'views/views.xml',
        'views/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
