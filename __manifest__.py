# -*- coding: utf-8 -*-
{
    'name': "tk_construction_salesfeature",

    'summary': """
        Allows to create Job costings right from Sales/Quotations module """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Mikhail Belogortsev",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'tk_construction_management', 'sale'],

    # always loaded
    'data': [
      #  'security/ir.model.access.csv',
        'views/extend_sale_order.xml',
        'views/templates.xml',
    ],

}
