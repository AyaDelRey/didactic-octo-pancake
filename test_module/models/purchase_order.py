# custom_addons/mon_module/models/purchase_order.py
from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def export_to_edi(self):
        # ici tu mets le code d’export
        for order in self:
            # ... code d’export EDI ...
            pass
