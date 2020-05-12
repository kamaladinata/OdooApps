# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" class respartner"""

from odoo import api, fields, models, _
from datetime import datetime
from odoo.osv.expression import get_unaccent_wrapper
import uuid


class ResPartner(models.Model):
    """Inherit ResPartner"""
    _name = "res.partner"
    _inherit = ['res.partner', 'portal.mixin']

    def _get_default_access_token(self):
        return str(uuid.uuid4())

    is_member = fields.Boolean(string="Is a Member")
    is_email_verified = fields.Boolean(string="Email Verified")
    access_token = fields.Char('Security Token', copy=False, default=_get_default_access_token)

    @api.multi
    def write(self, vals):
        """this extend function for edit partner"""
        # check email
        if 'email' in vals:
            vals['is_email_verified'] = False
        res = super(ResPartner, self).write(vals)
        return res
    
    @api.multi
    def send_email_verification(self):
        '''
        This function opens a window to compose an email, with the edit partner email verificaton template message loaded by default
        '''
        self.ensure_one()
        self._generate_access_token()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('email_verification', 'email_template_edit_partner_verification')[1]
        except ValueError:
            template_id = False
        
        if template_id:
            template_id = self.env['mail.template'].browse(template_id)
            template_id.send_mail(self.id, force_send=True)

        return True
        
    @api.multi
    def get_access_action(self, access_uid=None):
        """ Instead of the classic form view, redirect to the online order for
        portal users or if force_website=True in the context. """
        # TDE note: read access on sales order to portal users granted to followed sales orders
        self.ensure_one()

        user, record = self.env.user, self
        if access_uid:
            user = self.env['res.users'].sudo().browse(access_uid)
            record = self.sudo(user)
        if user.share or self.env.context.get('force_website'):
            try:
                record.check_access_rule('read')
            except AccessError:
                if self.env.context.get('force_website'):
                    return {
                        'type': 'ir.actions.act_url',
                        'url': '/my/orders/%s' % self.id,
                        'target': 'self',
                        'res_id': self.id,
                    }
                else:
                    pass
            else:
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/my/orders/%s?access_token=%s' % (self.id, self.access_token),
                    'target': 'self',
                    'res_id': self.id,
                }
        
        return super(ResPartner, self).get_access_action(access_uid)

    def get_mail_url(self):
        return self.get_share_url()

    def _generate_access_token(self):
        for order in self:
            order.access_token = self._get_default_access_token()
