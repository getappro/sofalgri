# -*- coding: utf-8 -*-
import logging
from datetime import date
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        _logger.info("-> Intercepting button_validate on picking ID %s (v5 - Per Product)", self.id)

        if self.picking_type_code == 'incoming':
            # 1. Identifier les lignes qui nécessitent un lot et qui n'en ont pas encore.
            lines_to_process = self.move_line_ids.filtered(
                lambda ml: ml.product_id.tracking == 'lot' and not ml.lot_name and ml.quantity > 0
            )

            if lines_to_process:
                # Vérification du fournisseur en amont
                if not self.partner_id or not self.partner_id.ref:
                    _logger.error("Validation failed: Partner %s has no internal reference.", self.partner_id.name)
                    raise UserError(
                        _("Le fournisseur '%s' doit avoir une référence interne (champ Réf) pour générer le numéro de lot.") % (
                            self.partner_id.name))

                # 2. Identifier les produits uniques parmi ces lignes.
                unique_products = lines_to_process.product_id
                _logger.info("Found %d unique product(s) that require lot numbers: %s", len(unique_products),
                             unique_products.mapped('display_name'))

                # 3. Boucler sur chaque produit unique.
                for product in unique_products:
                    # 4. Générer UN nouveau numéro de lot pour ce produit.
                    sequence = self.env['ir.sequence'].next_by_code('lot.receipt.sequence') or '00'
                    partner_ref = self.partner_id.ref
                    today_str = date.today().strftime('%d%m%Y')
                    new_lot_name = f"{sequence}{partner_ref}{today_str}"

                    _logger.info("Generated lot name '%s' for Product: %s", new_lot_name, product.display_name)

                    # 5. Trouver toutes les lignes pour CE produit spécifique.
                    lines_for_this_product = lines_to_process.filtered(lambda l: l.product_id == product)

                    # Assigner le nouveau nom de lot à toutes ces lignes.
                    lines_for_this_product.write({'lot_name': new_lot_name})

                    _logger.info("Assigned lot '%s' to %d line(s) for this product.", new_lot_name,
                                 len(lines_for_this_product))

        _logger.info("-> Calling original button_validate for picking ID %s", self.id)
        return super(StockPicking, self).button_validate()