from odoo import fields, models , api , _
from odoo.exceptions import UserError


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    @api.model
    def get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        active_origin = product_id.active if product_id else False
        if not active_origin:
            product_id.active = True
        res = super(ReportBomStructure, self).get_bom(bom_id,product_id,line_qty,line_id,level)

        if not active_origin and product_id:
            product_id.active = False

        return res