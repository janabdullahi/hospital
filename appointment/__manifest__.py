# -*- coding: utf-8 -*-
{
    'name': "appointment",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Hamed Jan",
    # 'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'patient'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
    ],
}

