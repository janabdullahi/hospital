from odoo import http
from odoo.http import request
from markupsafe import Markup

class AppointmentController(http.Controller):
    @http.route('/appointment/confirm/<int:appointment_id>', auth='public', type='http', website=True)
    def confirm_appointment(self, appointment_id):
        appointment = request.env['appointment.appointment'].sudo().browse(appointment_id)
        appointment.write({'state': 'confirmed'})
        appointment.message_post(
            body=Markup("<p>Appointment <strong style='color:green;'>Confirmed ✅ by Patient</strong></p>"),
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        return """
            <html>
            <body style="font-family:Arial; text-align:center; padding:50px;">
                <h1 style="color:green;">✅ Appointment Confirmed!</h1>
                <p>Thank you! Your appointment has been confirmed successfully.</p>
                <p>We look forward to seeing you.</p>
            </body>
            </html>
        """

    @http.route('/appointment/reject/<int:appointment_id>', auth='public', type='http', website=True)
    def reject_appointment(self, appointment_id):
        appointment = request.env['appointment.appointment'].sudo().browse(appointment_id)
        appointment.write({'state': 'cancelled'})
        appointment.message_post(
            body=Markup("<p>Appointment <strong style='color:red;'>Rejected ❌ by Patient</strong></p>"),
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        return """
            <html>
            <body style="font-family:Arial; text-align:center; padding:50px;">
                <h1 style="color:red;">❌ Appointment Rejected!</h1>
                <p>Your appointment has been cancelled.</p>
                <p>Please contact us to reschedule.</p>
            </body>
            </html>
        """