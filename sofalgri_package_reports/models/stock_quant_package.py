from odoo import models, fields, api


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    # Ajout du nouveau champ pour le poids à vide (tare)
    tare_weight = fields.Float(string='Poids à vide (Tare)')

    # Le champ shipping_weight est déjà existant, nous allons surcharger son calcul
    # Si le champ n'existait pas, vous le définiriez comme suit :
    shipping_weight = fields.Float(string='Poids Brut', compute='_compute_shipping_weight', store=True)

    @api.depends('tare_weight', 'quant_ids.quantity')
    def _compute_shipping_weight(self):
        """
        Calcule le poids d'expédition en déduisant le poids total des articles (quants)
        du poids à vide du contenant.
        """
        for package in self:
            # Calcule la somme des quantités des lignes stock.quant associées
            total_quantity = sum(quant.quantity for quant in package.quant_ids)

            # Calcule le poids d'expédition
            package.shipping_weight = package.tare_weight + total_quantity