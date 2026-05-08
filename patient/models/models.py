# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class patient(models.Model):
    _name = 'patient.patient'
    _description = 'patient.patient'

    patient_ref_No = fields.Char("Request Number", default='New', copy=False)
    name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
    dob = fields.Date(string="Date of Birth", default=fields.Date.context_today, required=True)
    place_of_birth = fields.Char('Place of Birth')
    country_of_birth = fields.Many2one("res.country", string="Country of Birth")
    nhs_number = fields.Integer("NHS Number")
    mrn_number = fields.Integer("MRN Number")
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
    emergency_contact = fields.Char("Contact Name")
    emergency_phone = fields.Char("Contact Phone")
    medical_history = fields.Html("Mdeical History")
    family_medical_history = fields.Html("Family Mdeical History")
    current_medication = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ], string="Current Medication", default="no")
    allergies = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ], string="Allergies" , default="no")
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('unspecified', 'Unspecified'),
        ], string="Blood Group" , default="unspecified")
    height = fields.Integer('Height(cm)')
    weight = fields.Integer('Weight')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_ref_No', 'New') == 'New':
                vals['patient_ref_No'] = self.env['ir.sequence'].next_by_code('patient.patient') or 'New'
        return super().create(vals_list)