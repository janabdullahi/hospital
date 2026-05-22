# -*- coding: utf-8 -*-

from odoo import models, fields, api


class appointmentslot(models.Model):
    _name = 'appointment.slot'

    name = fields.Char(required=True)
    capacity = fields.Integer(default=3)