# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description='Add fields to stock picking'

    driver_id = fields.Many2one(
        "res.partner",
        string="Driver",
    )
    matricule = fields.Char(
        string="Matricule Vehicule",
        store=True,
    )