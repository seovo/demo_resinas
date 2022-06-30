from odoo import fields, models , api , _
from odoo.exceptions import UserError
class StockMove(models.Model):
    _inherit = 'stock.move'
    solicitud_production_line = fields.Many2one('solicitud.production.line',string="SM")
    solicitud_production = fields.Many2one('solicitud.production',related='solicitud_production_line.order_id')
    stage_id = fields.Many2one('stage.mrpline', string="Etapa")
    should_consume_qty_store = fields.Float('Cantidad Original',
                                      digits='Product Unit of Measure')
    empaque_line = fields.Many2one('empaque.stock.mv', string="PT")

    is_valid_product_terminados = fields.Boolean()
    rs_empaque = fields.Float()
    rs_teorico = fields.Float()
    rs_teorico_kg = fields.Float()
    rs_real = fields.Float()
    rs_real_kg = fields.Float()
    rs_operativo = fields.Float()
    rs_operativo_kg = fields.Float()


    cost_subproducto = fields.Float(string="Costo")








