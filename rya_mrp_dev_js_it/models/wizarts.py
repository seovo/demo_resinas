from odoo import models, fields, api

class AlertasResinas(models.TransientModel):
	_name = 'alertas.resinas'
	qty = fields.Float(string="Cantidad")
