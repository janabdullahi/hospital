# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class department(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char('Department Name')
    doctor_ids = fields.One2many('doctor.doctor', 'department_id', string="Doctors")

    _sql_constraints = [
        ('unique_department_name',
        'unique(name)',
        'Department name must be unique!')
    ]