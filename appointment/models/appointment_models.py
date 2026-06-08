# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime


class appointment(models.Model):
    _name = 'appointment.appointment'
    _description = 'appointment.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    appointment_ref_No = fields.Char("Request Number", default='New', copy=False)
    patient_id = fields.Many2one('patient.patient', string='Patient Name', required=True)
    last_name = fields.Char(related='patient_id.last_name', readonly=True)
    dob = fields.Date(related='patient_id.dob', readonly=True)
    place_of_birth = fields.Char(related='patient_id.place_of_birth', readonly=True)
    country_of_birth = fields.Many2one("res.country", related='patient_id.country_of_birth', readonly=True)
    nhs_number = fields.Char(related='patient_id.nhs_number', readonly=True)
    mrn_number = fields.Char(related='patient_id.mrn_number', readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unspecified', 'Unspecified'),
        ], related='patient_id.gender', readonly=True)
    private_street = fields.Char(related='patient_id.private_street', readonly=True)
    private_street2 = fields.Char(related='patient_id.private_street2', readonly=True)
    private_city = fields.Char(related='patient_id.private_city', readonly=True)
    private_state_id = fields.Many2one("res.country.state", related='patient_id.private_state_id',
        domain="[('country_id', '=?', private_country_id)]", readonly=True)
    private_zip = fields.Char(related='patient_id.private_zip', readonly=True)
    private_country_id = fields.Many2one("res.country", related="patient_id.private_country_id", readonly=True)
    private_phone = fields.Char(related='patient_id.private_phone', readonly=True)
    private_email = fields.Char(related='patient_id.private_email', readonly=True)

    doctor_id = fields.Many2one('doctor.doctor', string='Doctor Name', required=True)
    doctor_last_name = fields.Char(related='doctor_id.last_name', required=True)
    doctor_dob = fields.Date(related='doctor_id.dob', required=True)
    doctor_country_of_birth = fields.Many2one("res.country", related='doctor_id.country_of_birth', required=True)
    doctor_index_number = fields.Char(related='doctor_id.doctor_index_number', required=True)
    gmc_ref_number = fields.Char(related='doctor_id.gmc_ref_number', required=True)
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('unspecified', 'Unspecified'),
        ], related='doctor_id.gender')
    doctor_private_phone = fields.Char(related='doctor_id.private_phone', required=True)
    doctor_private_email = fields.Char(related='doctor_id.private_email')
    doctor_private_street = fields.Char(related='doctor_id.private_street')
    doctor_private_street2 = fields.Char(related='doctor_id.private_street2')
    doctor_private_city = fields.Char(related='doctor_id.private_city')
    doctor_private_state_id = fields.Many2one(
        "res.country.state", related='doctor_id.private_state_id',
        domain="[('country_id', '=?', private_country_id)]",)
    doctor_private_zip = fields.Char(related='doctor_id.private_zip')
    doctor_private_country_id = fields.Many2one("res.country", related='doctor_id.private_country_id')
    appointment_date = fields.Date(string="Appointment Date", required=True)
    slot_id = fields.Many2one('appointment.slot', string='Time Slot', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", required=True, copy=False, default='draft')

    def cancel(self):
        for rec in self:
            rec.state = 'cancelled'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Cancelled!',
                'message': 'Appointment has been cancelled.',
                'type': 'warning',  
                'sticky': False,    
                
            }
        }


    def confirm(self):
        for rec in self:
            rec.state = 'confirmed'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Confirmed!',
                'message': 'Appointment has been confirmed successfully.',
                'type': 'success',  
                'sticky': False,    
                
            }
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('appointment_ref_No', 'New') == 'New':
                vals['appointment_ref_No'] = self.env['ir.sequence'].next_by_code('appointment.appointment') or 'New'
        return super().create(vals_list)

    @api.constrains('appointment_date', 'slot_id', 'patient_id', 'doctor_id')
    def _check_slot(self):
        for rec in self:
            # past dates
            if rec.appointment_date < date.today():
                raise ValidationError("You cannot book an appointment in the past.")
            # weekend booking
            if rec.appointment_date.weekday() in [5, 6]:
                raise ValidationError("Appointments are not available on weekends.")
            # same slot booking (any patient)
            count = self.search_count([
            ('appointment_date', '=', rec.appointment_date),
            ('slot_id', '=', rec.slot_id.id),
            ('id', '!=', rec.id)
            ])
            if count >= rec.slot_id.capacity:
                raise ValidationError(
                f"This slot allows only {rec.slot_id.capacity} patients.")
            # same patient same day
            duplicate_patient = self.search([
                ('patient_id', '=', rec.patient_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('id', '!=', rec.id)
            ])
            if duplicate_patient:
                raise ValidationError("This patient already has an appointment on this day.")
            # past slots current day
            if rec.appointment_date == date.today():
                current_hour = datetime.now().hour
                slot_hour = int(rec.slot_id.name.split(":")[0])
                if slot_hour <= current_hour:
                    raise ValidationError(
                        "You cannot book past time slots for today."
                    )
            duplicate_doctor = self.search([
                ('doctor_id', '=', rec.doctor_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('id', '!=', rec.id)
            ])
            if duplicate_doctor:
                raise ValidationError("This doctor already has an appointment on this slot.")