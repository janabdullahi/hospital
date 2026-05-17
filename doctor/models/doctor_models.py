# -*- coding: utf-8 -*-

from odoo import models, fields, api


class doctor(models.Model):
    _name = 'doctor.doctor'
    _description = 'doctor.doctor'

    name = fields.Char()