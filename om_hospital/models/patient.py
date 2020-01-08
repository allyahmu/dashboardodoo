from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = "Patient Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_name'

    class SaleOrderInherit(models.Model):
        _inherit = 'sale.order'
        patient_name = fields.Char(string='Patient Name')

    class ProductProduct(models.Model):
        _inherit = 'product.product'

        name = fields.Char()

    class ResPartner(models.Model):
        _inherit = 'res.partner'
        company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'OdooDev')])

    @api.multi
    def open_patient_appointment(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',

        }

    patient_name = fields.Char(string='Patient Name', required=True, track_visibility='always')
    patient_age = fields.Integer(string='Patient Age', track_visibility='always')
    patient_age2 = fields.Float(string='Patient Age Test')
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),

    ], string='Age Group', compute='set_age_group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string='Gender')
    address = fields.Char(string='Address', track_visibility='always')
    contact = fields.Char(string='Patient Contact', track_visibility='always')
    email_id = fields.Char(string='Email')
    image = fields.Binary(string='Upload Image')
    notes = fields.Text(string='Registration Notes')
    active = fields.Boolean('Active', default=True)
    name_seq = fields.Char(string="Patient ID", required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    doctor_id = fields.Many2one('doctor.list', string='Doctor Name')

    doctor_gender = fields.Selection([('male', 'Male'),
                                      ('fe_male', 'Female'),
                                      ], default='male', string="Doctor Gender")

    user_id = fields.Many2one('res.users', string='Pro Admin')
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name else False

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 8:
                raise ValidationError("The Age Must be Greater Than 8")

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient') or _('New')
            result = super(HospitalPatient, self).create(vals)
            return result

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s-%s' % (rec.name_seq, rec.patient_name)))
        return res

    @api.onchange('doc_id')
    def set_manager_gender(self):
        print("entring")
        for rec in self:
            if rec.doc_id:
                rec.doctor_gender = rec.doc_id.doctor_gender

    def action_send_card(self):
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
