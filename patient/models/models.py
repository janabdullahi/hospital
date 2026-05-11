# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class patient(models.Model):
    _name = 'patient.patient'
    _description = 'patient.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_ref_No = fields.Char("Request Number", default='New', copy=False)
    image_1920 = fields.Image(string="Profile Picture")
    name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)
    dob = fields.Date(string="Date of Birth", default=fields.Date.context_today, required=True)
    place_of_birth = fields.Char('Place of Birth', required=True)
    country_of_birth = fields.Many2one("res.country", string="Country of Birth", required=True)
    nhs_number = fields.Char("NHS Number",required=True)
    mrn_number = fields.Char("MRN Number")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unspecified', 'Unspecified'),
        ], string="Gender", default='unspecified')
    nationality_id = fields.Many2one('res.country', string='Nationality', required=True)
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
    private_phone = fields.Char(string="Private Phone", required=True)
    private_email = fields.Char(string="Private Email")
    emergency_contact = fields.Char("Contact Name", required=True)
    emergency_phone = fields.Char("Contact Phone", required=True)
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
        ], string="Blood Group" , default="unspecified", required=True)
    height = fields.Float('Height')
    cm_or_feet = fields.Selection([
        ('cm', 'Cm'),
        ('feet', 'Feet'),
        ], string="Cm / Feet" , default="cm")
    weight = fields.Float('Weight')
    kg_or_lbs = fields.Selection([
        ('kg', 'Kg'),
        ('lbs', 'lbs'),
        ], string="Kg / lbs" , default="kg")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_ref_No', 'New') == 'New':
                vals['patient_ref_No'] = self.env['ir.sequence'].next_by_code('patient.patient') or 'New'
        return super().create(vals_list)
    
    @api.constrains('nhs_number')
    def _check_nhs_number(self):
        for rec in self:
            if rec.nhs_number:
                # format check
                if not rec.nhs_number.isdigit() or len(rec.nhs_number) != 10:
                    raise ValidationError("NHS Number must be exactly 10 digits.")
                # duplicate check
            duplicate = self.search([
                ('nhs_number', '=', rec.nhs_number),
                ('id', '!=', rec.id)
            ])
            if duplicate:
                raise ValidationError("A patient already exists with this NHS number.")
                
# report
# kanban view(pic)
# user access