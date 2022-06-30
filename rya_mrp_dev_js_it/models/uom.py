from odoo import fields, models , api , _

class UomCategory(models.Model):
    _inherit = 'uom.category'
    is_empaque = fields.Boolean(string="Es Empaque")
    is_devolucion = fields.Boolean(string="Es Devolucion")