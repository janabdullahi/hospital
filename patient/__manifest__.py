# -*- coding: utf-8 -*-
{
    'name': "Patient management system",

    'summary': "Manage all patient records, personal details and medical information efficiently",

    'description': """
            Patient Management Module
            =========================

            This module provides a complete system to store, organise and manage all patient-related data within your healthcare or hospital management system.

            **Key Features:**

            - Store full patient details: first name, middle name, last name, date of birth, gender, contact information and address

            - Unique patient identification / registration number
            
            - Record emergency contact details
            
            - Track medical history, allergies and current conditions
            
            - Search, filter and sort patients easily
            
            - View and edit records through user-friendly forms and list views
            
            - Secure and centralised storage of patient data

            Perfect for clinics, hospitals or any medical facility that needs to maintain accurate, 
            structured patient information in one place.
    """,

    'author': "Hamed Jan",
    # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/patient_report.xml',
        'data/ir_sequence_data.xml',
        'views/views.xml',
    ],

    'assets': {
    'web.report_assets_common': [
        'patient/static/src/css/patient_report_design.css',
    ],
}
}

