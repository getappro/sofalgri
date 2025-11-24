# Copyright (C) 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    "name": "Sale Advance Payment",
    "version": "18.0.1.1.0",
    "author": "GetapPRO",
    "website": "https://www.getap.pro",
    "category": "Sales",
    "maintainers": ["GetapPRO"],
    "license": "AGPL-3",
    "summary": "Allow to add advance payments on sales orders",
    "depends": [
        "sale_management",
        "account",
    ],
    "data": [
        'data/ir_config_parameter.xml',
        'security/ir.model.access.csv',
        'wizards/sale_advance_payment_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/account_payment_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "installable": True,
}
