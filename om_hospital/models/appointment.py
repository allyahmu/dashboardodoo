from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment Record List'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'patient_date desc'

    _rec_name = 'patient_id'

    class SaleOrderInherit(models.Model):
        _inherit = 'sale.order'
        patient_name = fields.Char(string='Patient Name')

    def _get_default_note(self):
        return "Subscribe Your Channel and Like it!"

    patient_id = fields.Many2one('hospital.patient', string='Patient Name', required=True, track_visibility='onchange')
    patient_age = fields.Integer(string="Patient Age", required=True, related='patient_id.patient_age')
    patient_date = fields.Date(string='Date', required=True)
    reg_notes = fields.Text(string="Registration Notes", default=_get_default_note)
    name_seq = fields.Char(string="Appointment ID", required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),

    ], string='Status', readonly=True, default='draft')
    amount = fields.Float(string='Total Amount')
    patient_lines = fields.One2many('patient.appoint.lines', 'check_id', string='Check Patient Appointment Lines')
    notes = fields.Text(string='Student Service')
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    doctor_id = fields.Many2one('doctor.list', string='Doctor Name')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def delete_lines(self):
        for rec in self:
            print('rec', rec)
            rec.patient_lines = [(5, 0, 0)]

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code(
                'hospital.appointment') or _('New')
            result = super(HospitalAppointment, self).create(vals)
            return result

    def open_patient_appointment(self):
        return {
            'name': _('HospitalAppointments'),
            'domain': ['patient_id', '=', self.id],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'

        }

    class CheckPatientLines(models.Model):
        _name = 'patient.appoint.lines'
        _description = 'Check Patient Appointment Lines'
        product_id = fields.Many2one('product.product', string='Medicine')
        product_qty = fields.Integer(string='Quantity')

        check_id = fields.Many2one('hospital.appointment', string='Check ID')
