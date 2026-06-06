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
    doctor_id = fields.Many2one('doctor.doctor', string='Doctor Name', required=True)
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