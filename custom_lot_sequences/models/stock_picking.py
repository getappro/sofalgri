# -*- coding: utf-8 -*-
import logging
from datetime import date
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        _logger.info("-> Intercepting button_validate on picking ID %s", self.id)

        # Gestion des réceptions (incoming)
        if self.picking_type_code == 'incoming':
            lines_to_process = self.move_line_ids.filtered(
                lambda ml: ml.product_id.tracking == 'lot' and not ml.lot_name and ml.quantity > 0
            )

            if lines_to_process:
                if not self.partner_id or not self.partner_id.ref:
                    _logger.error("Validation failed: Partner %s has no internal reference.", self.partner_id.name)
                    raise UserError(
                        _("Le fournisseur '%s' doit avoir une référence interne (champ Réf) pour générer le numéro de lot.") % (
                            self.partner_id.name))

                unique_products = lines_to_process.product_id
                _logger.info("Found %d unique product(s) that require lot numbers: %s", len(unique_products),
                             unique_products.mapped('display_name'))

                for product in unique_products:
                    sequence = self.env['ir.sequence'].next_by_code('lot.receipt.sequence') or '00'
                    partner_ref = self.partner_id.ref
                    today_str = date.today().strftime('%d%m%Y')
                    new_lot_name = f"{sequence}{partner_ref}{today_str}"

                    _logger.info("Generated lot name '%s' for Product: %s", new_lot_name, product.display_name)

                    lines_for_this_product = lines_to_process.filtered(lambda l: l.product_id == product)
                    lines_for_this_product.write({'lot_name': new_lot_name})

                    _logger.info("Assigned lot '%s' to %d line(s) for this product.", new_lot_name,
                                 len(lines_for_this_product))

        # Note: La gestion des productions est maintenant faite dans MrpProduction.button_mark_done()

        _logger.info("-> Calling original button_validate for picking ID %s", self.id)
        return super(StockPicking, self).button_validate()


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _generate_lot_for_finished_product(self):
        """
        Générer automatiquement le lot du produit fini avant la validation
        """
        self.ensure_one()

        if self.product_id.tracking != 'lot':
            return

        # Récupérer les lots des composants
        component_lots = self.move_raw_ids.mapped('move_line_ids.lot_id').filtered(lambda l: l)

        if component_lots:
            # Extraire le numéro de séquence du premier lot de composant
            first_lot_name = component_lots[0].name
            sequence = first_lot_name[:4] if len(first_lot_name) >= 4 else '0000'
            _logger.info("Extracted sequence '%s' from component lot '%s'", sequence, first_lot_name)
        else:
            # Générer un nouveau numéro de séquence si aucun composant avec lot
            sequence = self.env['ir.sequence'].next_by_code('lot.receipt.sequence') or '0000'
            _logger.info("No component lots found, generated new sequence: %s", sequence)

        # Utiliser la date de production
        production_date = self.date_start.date() if self.date_start else date.today()
        date_str = production_date.strftime('%d%m%Y')

        # Générer le numéro de lot pour le produit fini
        new_lot_name = f"{sequence}S{date_str}"

        # Vérifier si le lot existe déjà
        existing_lot = self.env['stock.lot'].search([
            ('name', '=', new_lot_name),
            ('product_id', '=', self.product_id.id),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        if existing_lot:
            lot = existing_lot
            _logger.info("Using existing production lot '%s'", new_lot_name)
        else:
            # Créer le lot
            lot = self.env['stock.lot'].create({
                'name': new_lot_name,
                'product_id': self.product_id.id,
                'company_id': self.company_id.id,
            })
            _logger.info("Created production lot '%s' for product %s", new_lot_name, self.product_id.display_name)

        return lot

    def button_mark_done(self):
        """
        Intercepter la validation de l'ordre de production pour générer
        automatiquement le lot du produit fini AVANT l'appel au super
        """
        _logger.info("-> Intercepting button_mark_done on production ID %s", self.id)

        for production in self:
            if production.product_id.tracking == 'lot' and production.state not in ('done', 'cancel'):
                # Générer le lot avant la validation
                lot = production._generate_lot_for_finished_product()

                if lot:
                    # Assigner le lot à TOUS les move_line_ids du produit fini
                    # même ceux qui seront créés par le super
                    production.lot_producing_id = lot

                    # Si des lignes existent déjà, les mettre à jour
                    finished_move_lines = production.move_finished_ids.mapped('move_line_ids').filtered(
                        lambda ml: ml.product_id == production.product_id
                    )
                    if finished_move_lines:
                        finished_move_lines.write({'lot_id': lot.id})

        return super(MrpProduction, self).button_mark_done()