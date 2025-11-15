# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by GetapPRO.
# See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class SaleOrderTemplateLine(models.Model):
    _inherit = 'sale.order.template.line'

    # Logistics/Delivery fields
    product_packaging_id = fields.Many2one(
        comodel_name='product.packaging',
        string="Packaging",
        compute='_compute_product_packaging_id',
        store=True, readonly=False, precompute=True,
        domain="[('sales', '=', True), ('product_id','=',product_id)]",
        check_company=True)
    product_packaging_qty = fields.Float(
        string="Packaging Quantity",
        compute='_compute_product_packaging_qty',
        store=True, readonly=False, precompute=True)

    @api.depends('product_id', 'product_uom_qty', 'product_uom_id')
    def _compute_product_packaging_id(self):
        for line in self:
            # remove packaging if not match the product
            if line.product_packaging_id.product_id != line.product_id:
                line.product_packaging_id = False
            # suggest biggest suitable packaging matching the SO's company
            if line.product_id and line.product_uom_qty and line.product_uom_id:
                suggested_packaging = line.product_id.packaging_ids \
                    .filtered(lambda p: p.sales and (p.product_id.company_id <= p.company_id <= line.company_id)) \
                    ._find_suitable_product_packaging(line.product_uom_qty, line.product_uom_id)
                line.product_packaging_id = suggested_packaging or line.product_packaging_id

    @api.depends('product_packaging_id', 'product_uom_id', 'product_uom_qty')
    def _compute_product_packaging_qty(self):
        self.product_packaging_qty = 0
        for line in self:
            if not line.product_packaging_id:
                continue
            line.product_packaging_qty = line.product_packaging_id._compute_qty(line.product_uom_qty, line.product_uom_id)

    def _prepare_order_line_values(self):
        order_line_vals = super(SaleOrderTemplateLine, self)._prepare_order_line_values()
        if self.product_packaging_id:
            order_line_vals['product_packaging_id'] = self.product_packaging_id
            order_line_vals['product_packaging_qty'] = self.product_packaging_qty

        # 3. Retourner le dictionnaire modifié
        return order_line_vals
