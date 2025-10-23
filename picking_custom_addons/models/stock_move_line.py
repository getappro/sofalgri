# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    _description = 'Add fields for detailed weight calculation'

    # --- Champs existants pour le calcul final ---
    net_weight = fields.Float(
        string="Poids Net",
        digits='Stock Weight',
        help="Poids brut total mesuré sur la balance."
    )
    tare = fields.Float(
        string="Poids Tare",
        digits='Stock Weight',
        readonly=True,
        compute='_compute_tare',
        store=True,
        help="Poids total à vide (palette + caisses)."
    )

    # --- Nouveaux champs pour le calcul de la tare ---
    pallet_weight = fields.Float(
        string="Poids Palette",
        digits='Stock Weight',
        default=12.0,
        help="Poids de la palette vide."
    )
    crate_product_id = fields.Many2one(
        'product.product',
        string='Colis',
        domain="[('categ_id.name', '=', 'Colis')]",  # <-- DOMAIN AJOUTÉ ICI
        help="Sélectionnez le type de caisse utilisé (doit être un article avec un poids défini)."
    )

    # --- CHAMP AMÉLIORÉ ---
    # On remplace l'ancien champ Float et sa méthode onchange par un champ related.
    # C'est plus simple, plus rapide et plus fiable.
    crate_weight = fields.Float(
        string="Poids Caisse",
        related='crate_product_id.weight',  # <-- LA MAGIE EST ICI
        store=True,  # Important pour que le champ 'tare' puisse dépendre de lui
        readonly=True,
        digits='Stock Weight',
        help="Poids d'une seule caisse vide. Rempli automatiquement à la sélection de l'article caisse."
    )

    crate_quantity = fields.Float(
        string="Quantité Colis",
        default=0.0,
        help="Nombre total de caisses sur la palette."
    )

    # --- MÉTHODE ONCHANGE SUPPRIMÉE ---
    # La méthode _onchange_crate_product_id n'est plus nécessaire !

    @api.depends('pallet_weight', 'crate_quantity', 'crate_weight')
    def _compute_tare(self):
        """
        Calcule le poids total de la tare.
        Cette méthode fonctionne maintenant parfaitement car elle dépend de crate_weight
        qui est maintenant un champ 'related' et 'stored'.
        """
        for line in self:
            line.tare = line.pallet_weight + (line.crate_quantity * line.crate_weight)

    @api.onchange('net_weight', 'tare')
    def _onchange_weight_to_quantity(self):
        """
        Calcule la quantité finale (poids net du produit).
        """
        if self.net_weight > self.tare:
            self.quantity = self.net_weight - self.tare
        else:
            self.quantity = 0.0