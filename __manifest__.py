{
    'name': 'LMS Security Base',
    'version': '18.0.1.0.0',
    'summary': 'Base reusable de seguridad y control de accesos para modulos LMS',
    'description': """
Modulo base de seguridad para proyectos LMS en Odoo Community v18.
Incluye grupos base y mixin reutilizable para validacion de permisos.
""",
    'author': 'LMS',
    'website': '',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/lms_security_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}