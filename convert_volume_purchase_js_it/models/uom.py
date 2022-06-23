from odoo import fields, models , api , _

class UomCategory(models.Model):
    _inherit = 'uom.category'
    is_volume = fields.Boolean(string="Es Volumen")

class UomUom(models.Model):
    _inherit = 'uom.uom'
    is_volume = fields.Boolean(related="category_id.is_volume",string="Es Volumen")
    ratio_kg = fields.Float(digits=(13,10),string="Ratio KG")