# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class doctor(models.Model):
    _name = 'doctor.doctor'
    _description = 'Doctor record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    doctor_ref_No = fields.Char("Request Number", default='New', copy=False)
    image_1920 = fields.Image(string="Profile Picture")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    place_of_birth = fields.Char('Place of Birth', required=True)
    country_of_birth = fields.Many2one("res.country", string="Country of Birth", required=True)
    doctor_index_number = fields.Char('Doctor Index Number', required=True)
    gmc_ref_number = fields.Char('GMC Reference Number', required=True)
    nationality_id = fields.Many2one('res.country', string='Nationality', required=True)
    martial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('civil partnered', 'Civil Partnered'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated')
    ])
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unspecified', 'Unspecified'),
        ], string="Gender", default='unspecified')
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
    department_id = fields.Many2one('hospital.department')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('doctor_ref_No', 'New') == 'New':
                vals['doctor_ref_No'] = self.env['ir.sequence'].next_by_code('doctor.doctor') or 'New'
        return super().create(vals_list)
    
    @api.constrains('doctor_index_number','gmc_ref_number')
    def _check_doctor_index_or_gmc(self):
        # index format check
        for rec in self:
            if rec.doctor_index_number:
                if not rec.doctor_index_number.isdigit() or len(rec.doctor_index_number) != 6:
                    raise ValidationError("Doctor Index Number must be exactly 6 digits.")
        # gmc format check
        for rec in self:
            if rec.gmc_ref_number:
                if not rec.gmc_ref_number.isdigit() or len(rec.gmc_ref_number) != 7:
                    raise ValidationError("Doctor GMC Number must be exactly 7 digits.")

        # index duplicate check
            duplicate_index = self.search([
                ('doctor_index_number', '=', rec.doctor_index_number),
                ('id', '!=', rec.id)
            ])
            if duplicate_index:
                raise ValidationError("A doctor already exists with this Index number.")
        
        # gmc duplicate check
            duplicate_gmc = self.search([
                ('gmc_ref_number', '=', rec.gmc_ref_number),
                ('id', '!=', rec.id)
            ])
            if duplicate_gmc:
                raise ValidationError("A doctor already exists with this GMC number.")