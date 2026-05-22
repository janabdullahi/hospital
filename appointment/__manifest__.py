# -*- coding: utf-8 -*-
{
    'name': "Appointment Management",

    'summary': "Manage patient appointments and booking slots",

    'description': """
        Appointment Management Module

        This module helps manage patient appointments and booking schedules
        within the Odoo ERP system. It allows users to create and manage
        appointments, configure time slots, control slot capacity, and
        validate booking rules.

        Main Features:
        - Patient appointment booking
        - Time slot management
        - Slot capacity control
        - Prevent duplicate bookings
        - Prevent past date and past time bookings
        - Weekend booking restrictions
        - Appointment scheduling and tracking

        The module is designed to improve appointment handling,
        resource management, and booking efficiency.
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
        'views/appointment_views.xml',
    ],
}

