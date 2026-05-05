# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class patient(models.Model):
    _name = 'patient.patient'
    _description = 'patient.patient'

    patient_ref_No = fields.Char("Request Number", default='New', copy=False)
    name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
    dob = fields.Date(string="Date of birth", default=fields.Date.context_today, required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unspecified', 'Unspecified'),
        ], string="Gender", default='unspecified')
    nationality_id = fields.Many2one('res.country', string='Nationality')
    martial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('civil partnered', 'Civil Partnered'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated')
    ])
    private_street = fields.Char(string="Private Street")
    private_street2 = fields.Char(string="Private Street2")
    private_city = fields.Char(string="Private City")
    private_state_id = fields.Many2one(
        "res.country.state", string="Private State",
        domain="[('country_id', '=?', private_country_id)]",)
    private_zip = fields.Char(string="Private Zip")
    private_country_id = fields.Many2one("res.country", string="Private Country")
    private_phone = fields.Char(string="Private Phone")
    private_email = fields.Char(string="Private Email")
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_ref_No', 'New') == 'New':
                vals['patient_ref_No'] = self.env['ir.sequence'].next_by_code('patient.patient') or 'New'
        return super().create(vals_list)