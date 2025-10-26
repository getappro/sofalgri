# -*- coding: utf-8 -*-
from odoo import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    crate_quantity = fields.Float(
        string="Quantité de Caisses",
        related='package_id.crate_quantity',
        store=True, # store=True est essentiel pour pouvoir grouper et filtrer
        readonly=True
    )
    tare = fields.Float(
        string="Tare",
        digits='Stock Weight',
        help="Somme des tares accumulées pour ce colis."
    )