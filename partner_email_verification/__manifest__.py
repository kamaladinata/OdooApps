# -*- coding: utf-8 -*-

{
    'name': 'Partner Email Verification',
    'version': '11.0.0.1.9.1',
    'author': 'Kamal from Port Cities',
    'category': 'Contact',
    'summary': 'This is a custom module for Email Verification',
    'description': """
    v 1.0.0
        author : Kamal from Port Cities \n
        * Add feature Email Verification \n
    """,
    'depends': ['contacts', 'portal'],
    'data' : [
        'data/mail_template_data.xml',
        'views/res_partner_view.xml',
        'views/customer_portal_template.xml',
    ],
    'qweb': [],
    'active': False,
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 25.0,
    'sequence': 1,
    'currency': 'USD',
    'live_test_url': 'https://www.youtube.com/channel/UClhaCvCIq4NBghgjPtMu_pA',
}
