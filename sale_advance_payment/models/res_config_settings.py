# Copyright 2024 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_post_sale_advance_payments = fields.Boolean(
        config_parameter="sale_advance_payment.auto_post_advance_payments",
    )
    auto_reconcile_sale_advance_payments = fields.Boolean(
        config_parameter="sale_advance_payment.auto_reconcile_advance_payments",
    )