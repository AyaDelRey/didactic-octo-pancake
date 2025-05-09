# -*- coding: utf-8 -*-

# controllers/main.py
from odoo import http

class MonSite(http.Controller):
    @http.route('/contact_submit', type='http', auth='public', website=True)
    def contact_submit(self, nom=None, email=None, **kw):
        return "Merci, %s !" % nom

