# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    _description='Add fields to delivery Carrier'

    driver_id = fields.Many2one(
        "res.partner",
        string="Driver",
    )
    matricule = fields.Char(
        string="Matricule Vehicule",
        store=True,
    )