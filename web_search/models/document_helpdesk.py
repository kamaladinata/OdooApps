# -*- coding: utf-8 -*-
# Copyright: BMT ERP; Author: Alvin Adji.

from odoo import api, models, fields, _

class DocumentHelpdesk(models.Model):
    _name= 'document.helpdesk'
    _description = 'Document Helpdesk'


    helpdesk_id = fields.Many2one('helpdesk.ticket', string='Ticket')
    attachment = fields.Binary(string='Attachment')
    name = fields.Char(string='Document')