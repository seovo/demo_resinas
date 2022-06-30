# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.tools.float_utils import float_round, float_is_zero

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _match_all_variant_values(self, product_template_attribute_value_ids):
        if not self.active:
            return True
        return super(ProductProduct, self)._match_all_variant_values(product_template_attribute_value_ids)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_bom_count(self):
        for product in self:
            product.bom_count = self.env['mrp.bom'].search_count([
                ('product_tmpl_id', '=', product.id),'|',
                ('active','=',True),('active','=',False)
            ])