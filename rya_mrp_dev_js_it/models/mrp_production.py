from odoo import fields, models , api
from odoo.exceptions import UserError
from collections import defaultdict
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    plantilla_ratio = fields.Many2one('plantilla.ratios',string="Plantilla",ondelete='restrict')
    ratios = fields.One2many('mrp.ratios.lines','order_id')
    total_amount_ratios = fields.Float(compute="get_total_amount_ratios",store=True)
    product_qty_origin = fields.Float(string="Cantidad Original")
    mrp_bom_copy = fields.Many2one('mrp.bom')


    def calculate_new_cost_rs(self):
        res = self.env['report.rya_mrp_dev_js_it.index'].get_lines(self)
        res = res[0]
        #raise ValueError(str(res))
        cp =  0
        con_by = defaultdict(float)
        info_tm = []
        for m in self.move_finished_ids:
            info_tm.append(str(m.state)+"/"+str(m.product_uom_qty))
        #raise ValueError(info_tm)
        for l in self.move_finished_ids:
            if not l.state == 'done':
                continue
            if l.product_id == res['product']:
                cp += 1
                if cp > 1:
                    raise ValueError('mas de 2 producto principal')
                line_val = self.env['stock.valuation.layer'].search(
                    [('product_id', '=', l.product_id.id), ('stock_move_id', '=', l.id)])
                if not line_val:
                    raise ValueError('No se encontro una valoracion')
                #save origin cost
                if not  line_val.origin_unit_cost or  line_val.origin_unit_cost != 0:
                    line_val.origin_unit_cost = line_val.unit_cost
                if not line_val.origin_value or line_val.origin_value != 0:
                    line_val.origin_value = line_val.value

                avg_cost_unit = res['avg_cost_unit']
                avg_cost_tot = avg_cost_unit * line_val.quantity

                #avg_cost_unit
                line_val.unit_cost = avg_cost_unit
                line_val.value = avg_cost_tot

                l.is_valid_product_terminados = True
                l.rs_empaque = res['cost_empaque']
                l.rs_teorico = res['total_origin_unit']
                l.rs_teorico_kg = res['origin_x_kilo']
                l.rs_real = res['avg_cost_unit']
                l.rs_real_kg = res['avg_x_kilo']
                l.rs_operativo = res['total_operation_unit']
                l.rs_operativo_kg = res['operation_x_kilo']

            # FOR SUBPRODUCTS
            for sb in res['subproductos']:

                if l.product_id == sb['product']:
                    con_by[l.product_id] += 1
                    if con_by[l.product_id] > 1:
                        raise ValueError('mas de 2 sub  producto')
                    line_val_b = self.env['stock.valuation.layer'].search(
                        [('product_id', '=', l.product_id.id), ('stock_move_id', '=', l.id)])
                    if not line_val_b:
                        raise ValueError('No se encontro una valoracion')
                    # save origin cost
                    if not line_val_b.origin_unit_cost or line_val_b.origin_unit_cost != 0:
                        line_val_b.origin_unit_cost = line_val_b.unit_cost
                    if not line_val_b.origin_value or line_val_b.origin_value != 0:
                        line_val_b.origin_value = line_val_b.value

                    avg_cost_unit_b = sb['avg_cost_unit_by']
                    avg_cost_tot_b = avg_cost_unit_b * line_val_b.quantity

                    # avg_cost_unit
                    line_val_b.unit_cost = avg_cost_unit_b
                    line_val_b.value = avg_cost_tot_b

                    l.is_valid_product_terminados = True
                    l.rs_empaque = sb['cost_empaque']
                    l.rs_teorico = sb['total_origin_unit_by']
                    l.rs_teorico_kg = sb['total_origin_unit_kilo_by']
                    l.rs_real = sb['avg_cost_unit_by']
                    l.rs_real_kg = sb['avg_cost_unit_kilo_by']
                    l.rs_operativo = sb['total_operation_unit_by']
                    l.rs_operativo_kg = sb['total_operation_unit_kilo_by']

            costo_actual = 0
            cantidad_actual = 0
            for ij in self.env['stock.valuation.layer'].search([('product_id', '=', l.product_id.id)]):
                costo_actual += ij.value
                cantidad_actual += ij.quantity
            self.env.cr.execute("""update ir_property set value_float = """
                                + str(costo_actual / cantidad_actual if cantidad_actual != 0 else 0)
                                + """where name = 'standard_price' and company_id = """ + str(self.env.company.id)
                                + """ and res_id = 'product.product,""" + str(l.product_id.id) + """' """)




    def write(self, vals):
        res = super(MrpProduction, self).write(vals)
        try:
            # create empaque stock mv
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

        for l in self.move_raw_ids:
            if l.quantity_done > l.product_uom_qty:
                if not self.env['res.users'].has_group('rya_mrp_dev_js_it.mrp_permitir_mas_move'):
                    raise UserError('no esta permitido ingresar mas de lo reservado: '+l.product_id.display_name)



        for l in self.move_byproduct_ids:
            if l.quantity_done > l.product_uom_qty:
                if not self.env['res.users'].has_group('rya_mrp_dev_js_it.mrp_permitir_mas_move'):
                    raise UserError('no esta permitido ingresar mas de lo reservado: '+l.product_id.display_name)
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

        self.calculate_new_cost_rs()
        if self.bom_id:
            # duplicate bom list
            pt_copy = self.bom_id.product_tmpl_id.copy()
            pt_copy.active = False
            bom_copy = self.bom_id.copy()
            self.mrp_bom_copy = bom_copy.id
            bom_copy.product_tmpl_id = pt_copy
            bom_copy.product_id = False




        return res

    def show_list_material(self):
        return {
            'name': ('Lista Material Original'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.bom',
            #'views': [(view.id, 'form')],
            #'view_id': view.id,
            'target': 'current',
            'res_id': self.mrp_bom_copy.id,
            'context': dict(
                self.env.context,
            ),
        }




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