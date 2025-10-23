# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    total_net_weight = fields.Float(
        string="Poids Net Total",
        compute='_compute_total_weights',
        store=True,
        digits='Stock Weight',
        help="Somme des poids nets de toutes les lignes d'opérations détaillées."
    )
    total_tare = fields.Float(
        string="Tare Totale",
        compute='_compute_total_weights',
        store=True,
        digits='Stock Weight',
        help="Somme des tares de toutes les lignes d'opérations détaillées."
    )

    @api.depends('move_line_ids.net_weight', 'move_line_ids.tare')
    def _compute_total_weights(self):
        """
        Calcule et somme le poids net et la tare depuis les lignes d'opérations.
        """
        for move in self:
            move.total_net_weight = sum(move.move_line_ids.mapped('net_weight'))
            move.total_tare = sum(move.move_line_ids.mapped('tare'))