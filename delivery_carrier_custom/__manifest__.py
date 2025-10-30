# -*- coding: utf-8 -*-
{
    'name': 'Delivery Carrier Custom Addons',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Ajouter les personnalisations dans le mode de livraison',
    'description': """
        Ce module ajoute les champs et méthodes personnalisée pour Sofalgri.
    """,
    'depends': ['delivery','stock_delivery'],
    'data': [
        'views/delivery_carrier_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
