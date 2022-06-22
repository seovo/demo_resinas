from odoo import fields, models , api
from odoo.exceptions import UserError
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    plantilla_ratio = fields.Many2one('plantilla.ratios',string="Plantilla",ondelete='restrict')
    ratios = fields.One2many('mrp.ratios.lines','order_id')
    total_amount_ratios = fields.Float(compute="get_total_amount_ratios",store=True)
    product_qty_origin = fields.Float(string="Cantidad Original")


    def write(self, vals):
        res = super(MrpProduction, self).write(vals)
        try:
            result = self
            if result.move_byproduct_ids:
                for by in result.move_byproduct_ids:
                    dm = [('mrp_production_id', '=', result.id),
                          ('sub_producto', '=', by.id)]
                    exist = self.env['empaque.stock.mv'].search(dm)
                    if exist:
                        continue
                    vx = dict(
                        mrp_production_id=result.id,
                        sub_producto=by.id
                    )
                    self.env['empaque.stock.mv'].create(vx)
        except:
            return res

        return res
        

    @api.model
    def create(self, vals):
        result = super(MrpProduction, self).create(vals)
        try:
            vx = dict(
                mrp_production_id=result.id,
                mrp_production=result.id
            )
            self.env['empaque.stock.mv'].create(vx)

            if result.move_byproduct_ids:
                for by in result.move_byproduct_ids:
                    dm = [('mrp_production_id', '=', result.id),
                          ('sub_producto', '=', by.id)]
                    exist = self.env['empaque.stock.mv'].search(dm)
                    if exist:
                        continue
                    vx = dict(
                        mrp_production_id=result.id,
                        sub_producto=by.id
                    )
                    self.env['empaque.stock.mv'].create(vx)
        except:
            return result


        return result


    @api.depends('ratios','ratios.price_unit','ratios.quantity','ratios.price_total')
    def get_total_amount_ratios(self):
        for record in self:
            total = 0
            for r in record.ratios:
                total += r.price_total
            record.total_amount_ratios = total

    @api.onchange('qty_producing', 'lot_producing_id')
    def _onchange_producing(self):
        if self.state not in ['confirmed','progress','to_close']:
            self._set_qty_producing()

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        res = super(MrpProduction, self)._get_move_raw_values(product_id, product_uom_qty, product_uom, operation_id, bom_line)
        if bom_line:
            res['stage_id'] = bom_line.stage_id.id
        return res

    @api.model
    def default_get(self, fieldsx):
        res = super(MrpProduction, self).default_get(fieldsx)
        date_hoy = fields.Datetime.now()
        plantilla_default = self.env['plantilla.ratios'].search([
            ('period.date_start', '<=', date_hoy),('period.date_end', '>=', date_hoy)
        ])
        if plantilla_default:
            res.update({'plantilla_ratio': plantilla_default[0].id})
        return res


    def action_confirm(self):
        for l in self.move_byproduct_ids:
            if not l.product_uom_qty or l.product_uom_qty == 0:
                raise UserError('La cantidad de los subproductos no puede ser cero')
        self.product_qty_origin = self.product_qty
        for l in self.move_raw_ids:
            if not l.solicitud_production_line:
                l.should_consume_qty_store = l.product_uom_qty
            else:
                l.should_consume_qty_store = 0
        res = super(MrpProduction, self).action_confirm()
        return res



    @api.onchange('plantilla_ratio')
    def change_plantilla(self):
        for record in self:
            if record.plantilla_ratio:
                record.ratios.unlink()
                lines = record.plantilla_ratio.order_line
                for l in lines:
                    record.ratios += self.env['mrp.ratios.lines'].new({
                        'name': l.name ,
                        'price_unit': l.cost_projected
                    })

    def button_mark_done(self):

        for l in self.move_byproduct_ids:
            if not l.product_uom_qty or l.product_uom_qty == 0:
                raise UserError('La cantidad de los subproductos no puede ser cero')
            if not l.quantity_done or l.quantity_done == 0:
                raise UserError('La cantidad producida de los subproductos no puede ser cero')



        res = super(MrpProduction, self).button_mark_done()
        total_count = 0
        for l in self.move_byproduct_ids:
            total_count += l.quantity_done
            #l.change_qtyy()
        total_count += self.product_uom_qty
        for l in self.move_byproduct_ids:
            if total_count != 0:
                l.cost_share += (l.quantity_done / total_count) * 100

        return res




class PlantillaRatiosLine(models.Model):
    _name = 'mrp.ratios.lines'
    name = fields.Char(required=True)
    quantity = fields.Float(string="Cantidad",default=1)
    price_unit = fields.Float(string="Costo Unitario")
    price_total = fields.Float(string="Precio Total",compute="change_total")
    order_id = fields.Many2one('mrp.production', ondelete='restrict')
    @api.depends('quantity','price_unit')
    def change_total(self):
        for record in self:
            record.price_total = record.quantity * record.price_unit