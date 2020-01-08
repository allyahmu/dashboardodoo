from odoo import models, fields, api, _


class DoctorRecord(models.Model):
    _name = 'doctor.list'
    _description = 'Doctor Record List'

    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_name'

    class SaleOrderInherit(models.Model):
        _inherit = 'sale.order'

    doctor_name = fields.Char(string='Doctor Name')
    doctor_gender = fields.Selection([('male', 'Male'),
                                   ('fe_male', 'Female'),
                                   ], default='male', string="Doctor Gender")

    user_id = fields.Many2one('res.users', string='Related User')


