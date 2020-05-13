import json
from difflib import SequenceMatcher

from odoo import http, tools, _
from odoo.http import request


class WebsiteSale(http.Controller):
    @http.route(['/document/get_suggest'], type='http', auth="public", methods=['GET'], website=True)
    def get_suggest_json(self, **kw):
        query = kw.get('query')
        names = query.split(' ')
        domain = ['|' for k in range(len(names) - 1)] + [('name', 'ilike', name) for name in names]
        products = request.env['document.helpdesk'].search(domain, limit=30)
        products = sorted(products, key=lambda x: SequenceMatcher(None, query.lower(), x.name.lower()).ratio(),
                          reverse=True)
        results = []
        for product in products[0:15]:
            results.append({'value': product.name, 'data': {'id': product.id, 'after_selected': product.name}})
        return json.dumps({
            'query': 'Unit',
            'suggestions': results
        })
