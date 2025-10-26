# -*- coding: utf-8 -*-
{
    'name': 'Rapports de Colis SOFALGARI',
    'version': '18.0.1.1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Rapports personnalisés pour les colis de réception et remise en stock',
    'description': """
        Module pour générer des rapports de colis personnalisés :
        - Rapport de réception matière première
        - Rapport de remise en stock produits finis
    """,
    'author': 'GetapPRO',
    'website': 'https://www.getap.pro',
    'depends': ['base','stock', 'purchase', 'product','picking_custom_addons'],
    'data': [
        'data/report_paperformat.xml',
        'reports/package_reports.xml',
        'reports/package_report_templates.xml',
        'reports/picking_package_report_template.xml',
        'views/product_template_views.xml',
        'views/res_company_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}