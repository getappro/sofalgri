# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_truck_number = fields.Char(string='Matricule', help='Mettez le matricule de Camion de Livraison')

    def _prepare_invoice(self):
        """
        Surcharge de la méthode standard pour y ajouter notre champ personnalisé.
        """
        # 1. Appeler la méthode originale pour récupérer toutes les valeurs standards
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        # 2. Ajouter notre champ personnalisé au dictionnaire de valeurs
        #    La clé du dictionnaire doit correspondre au nom technique du champ
        #    dans le modèle account.move.
        if self.delivery_truck_number:
            invoice_vals['delivery_truck_number'] = self.delivery_truck_number

        # 3. Retourner le dictionnaire modifié
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit_package = fields.Float(
        string='Prix Unitaire/Colis',
        digits='Product Price',
    )

    # ... (vos méthodes @api.onchange restent inchangées, elles sont correctes) ...
    @api.onchange('product_packaging_id')
    def _onchange_product_packaging_id(self):
        """
        Au changement de conditionnement, on récupère le prix par défaut
        défini sur la fiche du conditionnement.
        """
        if self.product_packaging_id:
            # Récupérer le prix depuis le modèle product.packaging
            self.price_unit_package = self.product_packaging_id.unit_price_package
            # Mettre à jour le prix unitaire standard en conséquence
            if self.product_packaging_id.qty > 0:
                self.price_unit = self.product_packaging_id.unit_price_package / self.product_packaging_id.qty

    @api.onchange('price_unit_package')
    def _onchange_price_unit_package(self):
        """
        Si l'utilisateur modifie le prix par colis,
        on recalcule le prix unitaire standard.
        """
        if self.product_packaging_id and self.product_packaging_id.qty > 0:
            new_price_unit = self.price_unit_package / self.product_packaging_id.qty
            # Vérification pour éviter une boucle infinie de onchange
            if self.price_unit != new_price_unit:
                self.price_unit = new_price_unit

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        """
        Si l'utilisateur modifie le prix unitaire standard,
        on recalcule le prix par colis.
        """
        if self.product_packaging_id and self.product_packaging_id.qty > 0:
            new_price_unit_package = self.price_unit * self.product_packaging_id.qty
            # Vérification pour éviter une boucle infinie de onchange
            if self.price_unit_package != new_price_unit_package:
                self.price_unit_package = new_price_unit_package

    # --- MODIFICATION PRINCIPALE CI-DESSOUS ---
    def _prepare_invoice_line(self, **optional_values):
        """
        Surcharge de la méthode pour propager TOUS nos champs
        de la ligne de commande vers la ligne de facture.
        """
        # On appelle la méthode originale pour récupérer les valeurs par défaut
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        # On ajoute nos champs personnalisés
        res.update({
            'price_unit_package': self.price_unit_package,
            'product_packaging_id': self.product_packaging_id.id,
            'product_packaging_qty': self.product_packaging_qty,
        })
        return res