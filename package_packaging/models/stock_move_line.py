from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def write(self, vals):
        """
        Mettre à jour le conditionnement des quants quand
        le conditionnement change dans la ligne de mouvement
        """
        res = super(StockMoveLine, self).write(vals)

        if 'product_packaging_id' in vals or 'result_package_id' in vals:
            # Récupérer tous les quants impactés
            quants = self.env['stock.quant'].search([
                ('package_id', 'in', self.mapped('result_package_id').ids),
                ('product_id', 'in', self.mapped('product_id').ids)
            ])
            if quants:
                quants._compute_product_packaging()

        return res

    def _action_done(self):
        """
        Hook après la validation du mouvement pour calculer
        le conditionnement des quants créés
        """
        res = super(StockMoveLine, self)._action_done()

        # Mettre à jour les conditionnements des quants dans les packages
        packages = self.mapped('result_package_id').filtered(lambda p: p)
        if packages:
            quants = self.env['stock.quant'].search([
                ('package_id', 'in', packages.ids)
            ])
            quants._compute_product_packaging()

        return res

