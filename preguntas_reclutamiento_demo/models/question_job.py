from odoo import fields, models , api

class QuestionIT(models.Model):
    _name = 'question.js.it'
    name = fields.Text(string="Pregunta", required=True)
