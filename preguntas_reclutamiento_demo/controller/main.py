from odoo import http
from odoo.addons.payment.models.payment_acquirer import ValidationError
class ControlerQuestion(http.Controller):
    @http.route('/website_form_questions_hr', auth="public", methods=['POST'], website=True, csrf=False)
    def index(self,**post):
        raise ValidationError('que pasa')
        return post


