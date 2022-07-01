from odoo import http

class ControlerQuestion(http.Controller):
    @http.route('/website_form_questions_hr', auth="public", methods=['POST'], website=True, csrf=False)
    def index(self,**post):
        return post


