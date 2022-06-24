from odoo import fields, models , api , _

class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    ratio_kg = fields.Float(digits=(13,10),string="Ratio KG")
    unit_prove = fields.Many2one('uom.uom',domain=[('category_id.is_volume','=',True)],string="Und. Prove")
    cant_prov = fields.Float(string="Cant.Prov")
    prec_prov = fields.Float(string="Prec.Prov")

    @api.onchange('ratio_kg','unit_prove','prec_prov')
    def change_price_ps(self):
        for record in  self:
            record.product_qty = record.cant_prov * record.ratio_kg

            tot_tmp = record.cant_prov * record.prec_prov
            record.price_unit = tot_tmp / record.product_qty if record.product_qty != 0 else 0