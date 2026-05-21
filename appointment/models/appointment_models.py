# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime


class appointment(models.Model):
    _name = 'appointment.appointment'
    _description = 'appointment.appointment'

    patient_id = fields.Many2one('patient.patient', string='Patient Name', required=True)