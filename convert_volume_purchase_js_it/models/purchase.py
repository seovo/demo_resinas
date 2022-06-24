from odoo import fields, models , api , _

class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'
    is_volume = fields.Boolean(related="product_id.is_volume", string="Es Volumen")
    ratio_kg = fields.Float(digits=(13,10),string="Ratio KG")
    unit_prove = fields.Many2one('uom.uom',domain=[('category_id.is_volume','=',True)],string="Und. Prove")
    cant_prov = fields.Float(string="Cant.Prov")
    prec_prov = fields.Float(string="Prec.Prov")