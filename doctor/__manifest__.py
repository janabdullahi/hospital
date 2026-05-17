# -*- coding: utf-8 -*-
{
    'name': "Doctor Management System",

    'summary': "Manage doctor profiles, specialisations, schedules and professional information efficiently",

    'description': """
        Doctor Management Module
        ========================

        This module provides a complete system to store, organise and manage all doctor-related data within your healthcare or hospital management system.

        **Key Features:**

        - Store complete doctor information: first name, last name, gender, contact information and address

        - Manage doctor specialisations and departments

        - Maintain professional details including qualifications, experience and licence information

        - Assign doctors to patients, appointments and medical departments

        - Search, filter and sort doctor records easily

        - View and edit records through user-friendly forms and list views

        - Secure and centralised storage of doctor data

        Perfect for clinics, hospitals or healthcare facilities that need to efficiently manage medical staff and doctor information in one organised system.
    """,

    'author': "Hamed Jan",
    # 'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'application': True,
    'installable': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_views.xml',
    ],
}

