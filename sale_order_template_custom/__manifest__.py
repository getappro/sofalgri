# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by GetapPRO.
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Order Template Custom',
    'version': '18.0.0.1',
    'summary': 'Add Missing fields to sale order template',
    'description': ''' This addons add packaging_id and packaging_qty to sale order template''',
    'category': 'Sales',
    'author': 'GetapPRO',
    'website': 'www.getap.pro',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_template_views.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}