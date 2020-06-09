import json
from difflib import SequenceMatcher

from odoo import http, tools, _
from odoo.http import request


class WebsiteSale(http.Controller):
    @http.route(['/document/get_suggest'], type='http', auth="public", methods=['GET'], website=True)
    def get_suggest_json(self, **kw):
        query = kw.get('query')
        names = query.split(' ')
        domain = ['|' for k in range(len(names) - 1)] + [('description', 'ilike', name) for name in names]
        documents = request.env['document.helpdesk'].search(domain, limit=30)
        documents = sorted(documents, key=lambda x: SequenceMatcher(None, query.lower(), x.description.lower()).ratio(),
                          reverse=True)
        results = []
        for document in documents[0:15]:
            results.append({'value': document.description, 'data': {'id': document.id, 'after_selected': document.description}})
        return json.dumps({
            'query': 'Unit',
            'suggestions': results
        })
