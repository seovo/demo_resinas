from odoo.exceptions import UserError
from odoo import fields, models , api
etapas = [('tall','Alto'),('medium','Medio'),('under','Bajo')]
class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    last_name_partner = fields.Char(string="Apellido")
    date_born = fields.Date(string="Fecha de Nacimiento")
    gender = fields.Selection([('men','Masculino'),('women','Mujer'),('other','Otro')],string="Genero")
    type_doc = fields.Selection([('dni','DNI'),('ce','CE'),('other','Otro')],string="Tipo de Documento")
    nro_doc = fields.Char(string="Nro Documento")
    nro_passport = fields.Char(string="Nro Pasaporte")
    height = fields.Char(string="Estatura")
    weight = fields.Char(string="Peso")
    nro_vaccines = fields.Char(string="Numero de Vacunas")
    residencia = fields.Char()
    agree_salary = fields.Boolean(string="Acepta el Salario")
    agree_schedule = fields.Boolean(string="Acepta el Horario y Dias Laborables")
    know_offimatic = fields.Selection(etapas,string="Cuenta con conocimiento en Informática")
    know_english = fields.Selection(etapas,string="Cuenta con conocimiento de Ingles")
    know_italic = fields.Selection(etapas, string="Cuenta con conocimiento de Italiano")
    have_licence_cond = fields.Boolean(string="Cuenta con licencia de conducir")
    type_antiquity_licence = fields.Text(string="Indica que tipo y antigüedad de la misma")
    notes_last_jobs = fields.Text(string="Comenta tu experiencia en las funciones mencionadas en el aviso")
    have_availability_travel = fields.Boolean(string="Cuenta con disponibilidad para viajar")
    #availability = fields.Date(string="Fecha Disponiv")
    availability_job = fields.Selection([
        ('now','Inmediatamente') , ('1wek','1 semana') , ('15days','15 Dias') , ('to_more','A más')
    ],string="Tipo Disponibilidad")
    requirements_avalaible = fields.Text(string="Requisitos Disponibles")
    grade_study_tec = fields.Selection([('unfinished','Inconcluso'),('student','EStudiante'),
                                     ('egresado','Egresado'),('graduado','Graduado')],
                                       string="Estudios Técnicos")
    grade_study_university = fields.Selection([('unfinished', 'Inconcluso'), ('student', 'EStudiante'),
                                        ('egresado', 'Egresado'), ('bachiller', 'Bachiller'),
                                        ('titulado','Titulado'),('magister','Magister'),
                                        ('doctor','Doctor')],string="Estudios Universitarios")
    additional_study = fields.Text(string="Cuentas con estudios en",
                                   help="poner cursos, maestrías, diplomados, especialidades,etc.")
    avalaible_change_residence = fields.Selection([('extranjero','Extranjero'),
                                                   ('national','Nacional'),('no','No')],
                                                  string="disponibilidad para cambio de residencia")
    reason_job = fields.Text(string="Indica por qué te gustaría trabajar con nosotros")
    doc_cv = fields.Binary(string="Documento CV")
    name_file_cv = fields.Char()


