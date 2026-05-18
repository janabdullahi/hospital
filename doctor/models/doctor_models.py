# -*- coding: utf-8 -*-

from odoo import models, fields, api


class doctor(models.Model):
    _name = 'doctor.doctor'
    _description = 'doctor.doctor'

    doctor_ref_No = fields.Char("Request Number", default='New', copy=False)
    image_1920 = fields.Image(string="Profile Picture")
    name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)
    dob = fields.Date(string="Date of Birth", default=fields.Date.context_today, required=True)
    place_of_birth = fields.Char('Place of Birth', required=True)
    country_of_birth = fields.Many2one("res.country", string="Country of Birth", required=True)
    image_1920 = fields.Image(string="Profile Picture")
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