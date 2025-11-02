# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Ajouter les champs manquant pour Sofalgri'

    eori_number = fields.Char(string="EORI Number")
    tax_code = fields.Char(string="Tax Code")
    btw_identification = fields.Char(string="Btw-identificatienummer NL")
    gln = fields.Char(string="GLN")

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    _description = 'Ajouter les champs manquant pour Sofalgri'

    code_swift = fields.Char(string="BIC – Code SWIFT")
    iban = fields.Char(string="IBAN")