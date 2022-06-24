from odoo import fields, models , api , _

class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'
    ratio_kg = fields.Float(digits=(13,10),string="Ratio KG")
    unit_prove = fields.Many2one('uom.uom',domain=[('category_id.is_volume','=',True)],string="Und. Prove")
    cant_prov = fields.Float(string="Cant.Prov")
    prec_prov = fields.Float(string="Prec.Prov")

    @api.onchange('product_id', 'unit_prove')
    def change_ratio(self):
        for record in self:
            ratio = 0
            for r in record.product_id.ratios_uom:
                if r.unit_prove == record.unit_prove:
                    ratio = r.ratio_kg

            record.ratio_kg = ratio

    @api.onchange('ratio_kg','prec_prov','cant_prov')
    def change_price_ps(self):
        for record in  self:
            qty = record.cant_prov * record.ratio_kg

            record.product_qty = qty

            tot_tmp = record.cant_prov * record.prec_prov
            record.price_unit = tot_tmp / qty if qty != 0 else 0

