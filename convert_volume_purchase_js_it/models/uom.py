from odoo import fields, models , api , _

class UomCategory(models.Model):
    _inherit = 'uom.category'
    is_volume = fields.Boolean(string="Es Volumen")

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    is_volume = fields.Boolean(related="uom_id.category_id.is_volume",string="Es Volumen")
    ratio_kg = fields.Float(digits=(13,10),string="Ratio KG")