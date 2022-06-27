from odoo.exceptions import UserError
from odoo import fields, models , api

class HrJob(models.Model):
    _inherit = 'hr.job'
    questions_test = fields.Many2many('question.js.it',string="Preguntas")