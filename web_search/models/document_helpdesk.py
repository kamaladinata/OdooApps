# -*- coding: utf-8 -*-
# Copyright: BMT ERP; Author: Alvin Adji.

from odoo import api, models, fields, _
import base64
from io import BytesIO

class DocumentHelpdesk(models.Model):
    _name= 'document.helpdesk'
    _description = 'Document Helpdesk'


    helpdesk_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    attachment = fields.Binary(string='Attachment')
    name = fields.Char(string='name')
    description = fields.Char(string='Document')

    def name_get(self):
        context = self._context
        if context is None:
            context = {}
        res = []
        for doc in self:
            res.append((doc.id, doc.description))
        return res

    @api.model
    def create(self, vals):
        res = super(DocumentHelpdesk, self).create(vals)
        attachment = self.env['ir.attachment']
        if vals.get('attachment', False):
            file_attach = attachment.create({
                'name': vals.get('name', False) or self.name,
                'datas': vals.get('attachment', False),
                'type': 'binary',
                'res_id': res.id,
                'res_model': 'document.helpdesk'
            })
                
        return res
    
    def write(self, vals):
        res = super(DocumentHelpdesk, self).write(vals)
        for doc in self:
            attachment = self.env['ir.attachment']
            if vals.get('attachment'):
                file_attach = attachment.create({
                    'name': vals.get('name', False) or self.name,
                    'datas': vals.get('attachment', False),
                    'type': 'binary',
                    'res_id': self.id,
                    'res_model': 'document.helpdesk'
                })
        return res