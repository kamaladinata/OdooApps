# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class VerificationEmail(http.Controller):

    def _get_partner(self, partner_id, token):
        partner = request.env['res.partner'].sudo().search([('id', '=', partner_id),('access_token', '=', token)], limit=1)
        return partner

    @http.route('/customer/portal/<int:partner_id>/<string:token>', type='http', auth="public")
    def check_email_verification(self, partner_id, token, **kwargs):
        partner = self._get_partner(partner_id, token)
        if partner.is_email_verified:
            return request.env['ir.ui.view'].render_template('partner_email_verification.partner_external_page_view', {
            'web_base_url': 'https://mail.google.com/'
        })
        return request.env['ir.ui.view'].render_template('partner_email_verification.partner_external_page_submit', {
            'token': token, 'partner_id': partner_id, 'email': partner.email,
        })
    
    @http.route('/customer/verified/<int:partner_id>/<string:token>', type="http", auth="public", methods=['post'])
    def action_verification(self, partner_id, token, **kwargs):
        partner = self._get_partner(partner_id, token)
        if partner:
            partner.is_email_verified = True
        return request.env['ir.ui.view'].render_template('partner_email_verification.partner_external_page_view', {
            'web_base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        })
