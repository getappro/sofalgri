from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Add fields package reports'

    product_variety = fields.Char(string="Variété")
    product_category = fields.Char(string="Catégorie")
    type_emballage = fields.Char(string="Type colis")
    qty_emballage = fields.Integer(string="Quantité par colis")
    global_gap = fields.Char(string="Global Gap Number")

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Add fields package reports'

    calibre = fields.Char(string="Calibre")