from odoo import http

from odoo.http import request
import requests
from datetime import datetime
import base64
from odoo.addons.payment.models.payment_acquirer import ValidationError
class ControlerQuestion(http.Controller):
    @http.route('/website_form_questions_hr', auth="public", methods=['POST'], website=True, csrf=False)
    def index(self,**post):
        data = dict()
        data['job_id'] = int(post['job_id'])
        try:
            data['department_id'] = int(post['department_id'])
        except:
            a = 1




        for p in post:
            domain = [('name','=',p),('model_id.model','=','hr.applicant')]


            campo = http.request.env['ir.model.fields'].sudo().search(domain)

            if campo:
                if campo.ttype in ['char','text','selection']:
                    data[p] = str(post[p])
                    if campo.name == 'partner_name':
                        data['name'] = 'Solicitud de '+str(post[p])
                        data['name_file_cv'] = 'CV_'+str(post[p])
                if campo.ttype in ['date']:
                    #raise ValidationError(post[p])
                    fecha = datetime.strptime(str(post[p]), '%Y-%m-%d')
                    data[p] = fecha
                if campo.ttype in ['binary']:
                    archivo = base64.b64encode(post.get(p).read())
                    data[p]= archivo

                if campo.ttype in ['boolean']:
                    data[p] = True if post[p] == 'on' else False


        #raise ValidationError(data)

        http.request.env['hr.applicant'].sudo().create(data)
        return http.request.render("questions_jobs_personalized_js_it.thankyou")
        return True