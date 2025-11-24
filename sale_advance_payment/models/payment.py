# Copyright (C) 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sale Order",
        readonly=True,
        index=True,
    )