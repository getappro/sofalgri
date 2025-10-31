# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Add fields package reports'

    number_export = fields.Char(string="N° Exportateur")
    number_ggn = fields.Char(string="N° GGN")
    number_onsa = fields.Char(string="N° autorisation ONSA")
    coc_export = fields.Char(string="CoC Exportateur")

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Add fields package reports'

    number_station = fields.Char(string="N° Station")
    coc_station = fields.Char(string="CoC Station")