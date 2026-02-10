from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_invoice(self):
        # 1. Appeler la méthode standard pour créer la facture fournisseur (le 'Bill')
        res = super(PurchaseOrder, self).action_create_invoice()
        
        # Le retour de super() est souvent une action pour ouvrir la vue de la facture
        # Nous allons boucler sur les factures liées à ce bon de commande
        for order in self:
            # On récupère les factures au statut 'draft' liées à cette commande
            # (celles qui viennent d'être créées)
            new_bills = order.invoice_ids.filtered(lambda m: m.state == 'draft' and m.move_type == 'in_invoice')
            
            for bill in new_bills:
                # 2. Remplir la date de facture avec la date de confirmation de la commande
                # Sur purchase.order, la date de validation est 'date_approve'
                if order.date_approve:
                    bill.write({
                        'invoice_date': order.date_approve.date()
                    })
                
                # 3. Valider la facture (Passer de Brouillon à Affiché/Ouvert)
                bill.action_post()

                # 4. Enregistrer le paiement en espèces
                self._register_automatic_cash_payment(bill)
        
        return res

    def _register_automatic_cash_payment(self, bill):
        """ Crée et valide le paiement en espèces pour la facture fournisseur """
        # Trouver le journal de type 'espèces' (cash)
        journal = self.env['account.journal'].search([
            ('type', '=', 'cash'),
            ('company_id', '=', bill.company_id.id)
        ], limit=1)

        if not journal:
            # On ne bloque pas le processus si le journal cash n'existe pas,
            # mais on pourrait ajouter un log ou une notification
            return

        # Utilisation du wizard de paiement pour Odoo 18
        payment_register = self.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=bill.ids
        ).create({
            'journal_id': journal.id,
            'payment_date': bill.invoice_date,
            'amount': bill.amount_total,
            # Pour un fournisseur, le type de paiement est 'outbound' (sortant)
            # Odoo le gère automatiquement via le wizard basé sur le move_type 'in_invoice'
        })

        # Création et validation du paiement (lettrage automatique)
        payment_register.action_create_payments()
