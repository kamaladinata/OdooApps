# -*- coding: utf-8 -*-
##############################################################################
#
# This module is developed by Portcities Indonesia
# Copyright (C) 2018 Portcities Indonesia (<http://idealisconsulting.com>).
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import get_records_pager, pager as portal_pager, CustomerPortal
from odoo.addons.helpdesk.controllers.portal import CustomerPortal
from odoo.osv.expression import OR

from odoo.addons.portal.controllers.mail import PortalChatter
from odoo.tools import plaintext2html


class MyDocumentPortal(CustomerPortal):

    @http.route(['/my/document', '/my/document/page/<int:page>'], type='http', auth="user", website=True)
    def my_document_list(self, page=1, date_begin=None, date_end=None, sortby=None, search=None, search_in='all', **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Subject'), 'order': 'name'},
        }
        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
            'file': {'input': 'file', 'label': _('Search in Filename')},
            'ticket': {'input': 'ticket', 'label': _('Search in Ticket')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('document.helpdesk', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('description', 'ilike', search)]])
            if search_in in ('file', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            # if search_in in ('message', 'all'):
            #     search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            domain += search_domain

        # pager
        tickets_count = request.env['document.helpdesk'].search_count(domain)
        pager = portal_pager(
            url="/my/document",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=tickets_count,
            page=page,
            step=self._items_per_page
        )

        tickets = request.env['document.helpdesk'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]

        values.update({
            'date': date_begin,
            'tickets': tickets,
            'page_name': 'Document Helpdesk',
            'default_url': '/my/document',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'sortby': sortby,
            'search_in': search_in,
            'search': search,
            'title': 'Search Documents'
        })
        
        return request.render("web_searchbar.portal_document_helpdesk", values)

    @http.route([
        "/my/hh/<int:ticket_id>",
        "/my/hh/<int:ticket_id>/<token>"
    ], type='http', auth="public", website=True)
    def hh_tickets_followup(self, ticket_id, token=None):
        Ticket = False
        if token:
            Ticket = request.env['document.helpdesk'].sudo().search([('id', '=', ticket_id), ('access_token', '=', token)])
        else:
            Ticket = request.env['document.helpdesk'].sudo().browse(ticket_id)
        if not Ticket:
            return request.redirect('/my/hh')
        values = {'ticket': Ticket}
        history = request.session.get('my_tickets_history', [])
        hh_records_pager = get_records_pager(history, Ticket)
        # rewrite return address(prev and next record) for hh
        prev_record = hh_records_pager.get('prev_record')
        next_record = hh_records_pager.get('next_record')
        idx_prev_record = prev_record and (prev_record.rfind("/") + 1)
        idx_next_record = next_record and (next_record.rfind("/") + 1)

        hh_idx_prev_record = idx_prev_record and prev_record[idx_prev_record:]
        hh_idx_next_record = idx_next_record and next_record[idx_next_record:]

        hh_records_pager.update({
            'prev_record': str("/my/hh/"+hh_idx_prev_record) if hh_idx_prev_record else False,
            'next_record': str("/my/hh/"+hh_idx_next_record) if hh_idx_next_record else False
        })

        values.update(hh_records_pager)
        return request.render("web_searchbar.document_followup", values)