from odoo import models, fields, api

class AlertasResinas(models.TransientModel):
    _name = 'alertas.resinas'
    mrp_production = fields.Many2one('mrp.production')
    msg = fields.Html()
    def confirm_continue(self):
        return self.mrp_production.with_context(wizard_rs_no=True).button_mark_done()
