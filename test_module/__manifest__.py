# -*- coding: utf-8 -*-
{
    'name': "test_module",
    'summary': "Module de test avec page web et formulaire de contact",
    'description': """
Ce module ajoute une page web personnalisée avec un formulaire de contact.
""",
    'author': "AyaDelRey",
    'website': "https://github.com/AyaDelRey",
    'category': 'Website',
    'version': '1.0',

    'depends': ['base', 'website'],  # ajoute 'website' pour activer le builder

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
}
