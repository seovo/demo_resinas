from odoo import fields, models , api

FIELD_TYPES = [(key, key) for key in sorted(fields.Field.by_type)]
'''
FIELD_TYPES = [
    ('binary','Binario'),
    ('boolean','Booleano'),
    ('char','Caracter'),
    ('date','Fecha'),
    ('datetime','Fecha y Hora'),
    ('float','Numero Flotante'),
    ('html','HTML'),
    ('integer','Entero') ,
    ('monetary','MOnetario'),
    ('reference','Referencia'),
    ('selection','Seleccion'),
    ('text','Texto')
]
'''
class QuestionIT(models.Model):
    _name = 'question.js.it'
    name = fields.Text(string="Pregunta",required=True)
    ttype = fields.Selection(FIELD_TYPES, string='Field Type', required=True)
    field_id = fields.Many2one('ir.model.fields', string="Campo Relacionado")
    sequence = fields.Integer()
    is_email = fields.Boolean(string="Es un Correo",default=False)

