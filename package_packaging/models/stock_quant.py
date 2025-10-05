from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_packaging_id = fields.Many2one(
        'product.packaging',
        string='Conditionnement',
        compute='_compute_product_packaging',
        store=True,
        help="Conditionnement utilisé lors de la mise en package"
    )

    product_packaging_qty = fields.Float(
        string='Qté Conditionnement',
        compute='_compute_product_packaging',
        store=True,
        digits='Product Unit of Measure',
        help="Quantité de conditionnements"
    )

    @api.depends('package_id', 'product_id', 'quantity')
    def _compute_product_packaging(self):
        """
        Récupère le conditionnement depuis les mouvements de stock
        qui ont créé ce quant dans le package et calcule la quantité
        """
        for quant in self:
            packaging = False
            packaging_qty = 0.0

            if quant.package_id and quant.product_id:
                # Chercher dans les mouvements de stock (result_package_id)
                move_line = self.env['stock.move.line'].search([
                    ('result_package_id', '=', quant.package_id.id),
                    ('product_id', '=', quant.product_id.id),
                    ('product_packaging_id', '!=', False),
                    '|',
                    ('lot_id', '=', quant.lot_id.id if quant.lot_id else False),
                    ('lot_id', '=', False)
                ], limit=1, order='id desc')

                if move_line:
                    packaging = move_line.product_packaging_id
                    # Calculer la quantité de conditionnements
                    if packaging and packaging.qty > 0:
                        packaging_qty = quant.quantity / packaging.qty

            quant.product_packaging_id = packaging
            quant.product_packaging_qty = packaging_qty
