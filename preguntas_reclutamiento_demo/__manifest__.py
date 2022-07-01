# -*- encoding: utf-8 -*-
{
    'name': 'Preguntas Perzonalizado',
    'category': 'uncategorize',
    'author': 'FULL STACK DEMO',
    'depends': ['website_hr_recruitment'],
    'version': '1.0',
    'description':"""
     Descripcion DEL MODULO
    """,
    'auto_install': False,
    'demo': [],
    'data': [
          'security/ir.model.access.csv',
          'views/question_job.xml',
          'views/hr_job.xml'
        ],
    'installable': True
}