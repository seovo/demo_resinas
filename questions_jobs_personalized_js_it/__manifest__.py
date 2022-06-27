# -*- encoding: utf-8 -*-
{
    'name': 'Preguntas Perzonalizado',
    'category': 'uncategorize',
    'author': 'ITGRUPO',
    'depends': ['website_hr_recruitment','base'],
    'version': '1.0',
    'description':"""
     Descripcion
    """,
    'auto_install': False,
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/question_jobs.xml',
        'views/hr_applicant.xml',
        'data/question.xml',
        'views/hr_job.xml',
        'views/templates.xml'

        ],
    'installable': True
}