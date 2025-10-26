# -*- coding: utf-8 -*-
from odoo import models, fields

class StockPackageType(models.Model):
    _inherit = 'stock.package.type'
    # Vous pouvez ajouter des infos par défaut ici si besoin plus tard
    pass

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    crate_quantity = fields.Float(
        string="Quantité de Caisses",
        help="Nombre total de caisses sur ce colis/cette palette."
    )
    tare = fields.Float(
        string="Tare",
        digits='Stock Weight',
        help="Somme des tares accumulées pour ce colis."
    )
    packaging_datetime = fields.Datetime(
        string="Date et Heure de Colisage",
        copy=False,  # On ne copie pas cette valeur si le colis est dupliqué
        help="Date et heure exactes de la dernière opération de colisage."
    )