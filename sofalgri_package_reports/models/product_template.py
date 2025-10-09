# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Add fields package reports'

    product_variety = fields.Char(string="Variété")
    product_classify = fields.Selection([('1', '1'), ('2', '2')],
                              string='Classe Produit', default='1')
    global_gap = fields.Char(string="Global Gap Number")

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Add fields package reports'

    calibre = fields.Char(string="Calibre")