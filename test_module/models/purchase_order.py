from odoo import models, api
import os
import datetime
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def export_to_edi(self):
        """ Export des bons de commande au format EDI et envoi par email. """

        export_dir = '/tmp/edi_exports'
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        mail_mail = self.env['mail.mail']

        for order in self:
            filename = f"PO_{order.name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.edi"
            filepath = os.path.join(export_dir, filename)

            lines = []
            lines.append(f"PO|{order.name}|{order.date_order.strftime('%Y%m%d')}|{order.partner_id.name}")
            for line in order.order_line:
                product = line.product_id.default_code or line.product_id.name
                qty = line.product_qty
                price = line.price_unit
                lines.append(f"LI|{product}|{qty}|{price:.2f}")
            lines.append(f"END|{len(order.order_line)}|{order.amount_total:.2f}")

            with open(filepath, 'w') as f:
                f.write('\n'.join(lines))

            # Lecture du contenu pour la pièce jointe (en base64)
            with open(filepath, 'rb') as f:
                file_data = f.read()
            import base64
            file_base64 = base64.b64encode(file_data)

            # Vérification que le partenaire a un email
            if not order.partner_id.email:
                raise UserError(f"Le fournisseur {order.partner_id.name} n'a pas d'email défini.")

            # Création du mail
            mail_vals = {
                'subject': f'Export EDI - Bon de commande {order.name}',
                'body_html': f"<p>Bonjour {order.partner_id.name},</p><p>Veuillez trouver en pièce jointe le bon de commande {order.name} au format EDI.</p>",
                'email_to': order.partner_id.email,
                'attachment_ids': [(0, 0, {
                    'name': filename,
                    'type': 'binary',
                    'datas': file_base64.decode('utf-8'),
                    'mimetype': 'text/plain',
                })],
            }

            mail = mail_mail.create(mail_vals)
            mail_mail.send(mail)

        return True
