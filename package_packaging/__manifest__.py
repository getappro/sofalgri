# -*- coding: utf-8 -*-
{
    'name': 'Package Packaging Display',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Afficher le conditionnement des produits dans les packages',
    'description': """
        Ce module permet d'afficher le conditionnement des produits 
        dans la vue formulaire des packages (stock.quant.package).
    """,
    'depends': ['stock', 'product'],
    'data': [
        'views/stock_quant_package_views.xml',
        'views/stock_quant_tree_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
