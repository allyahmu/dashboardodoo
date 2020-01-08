from odoo import models, fields, api, _


class CheckCreateAppointment(models.TransientModel):
    _name = 'hospital_create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    patient_date = fields.Date(string='Appointment Date')

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'patient_date': self.patient_date,
            'reg_notes': 'Created From Avery Hmu'

        }
        # Creating Appointments From the Code
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context

                }
        self.patient_id.message_post(body="Check Appointment Created Successfully", subject="Appointment Creation")
        self.env['hospital.appointment'].create(vals)

    def get_data(self):
        print("Get Data Function")
        appointments = self.env['hospital.appointment'].search([])
        print("appointments", appointments)
        for rec in appointments:
            print("Appointment Name", rec.name_seq)
