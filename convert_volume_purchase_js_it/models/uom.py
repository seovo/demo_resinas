from odoo import fields, models , api , _

class UomCategory(models.Model):
    _inherit = 'uom.category'
    is_volume = fields.Boolean(string="Es Volumen")

class RatiosRatios(models.Model):
    name = 'ratios.ratios.tmp'
    product_id = fields.Many2one('product.template')
    unit_prove = fields.Many2one('uom.uom', domain=[('category_id.is_volume', '=', True)],
                                 string="Und. Prove",required=True)
    ratio_kg = fields.Float(digits=(13, 10), string="Ratio KG")

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    ratios_ids = fields.One2many('ratios.ratios.tmp','product_id')

