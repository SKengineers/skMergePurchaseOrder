# -*- coding: utf-8 -*-
{
    'name': "SK odoo Merge Purchase Order",
    'summary': """
        Merge Purchase Order""",
    'description': """
        Merge Purchase Order
            """,
    'author': 'Sritharan K',
    'company': 'SKengineer',
    'maintainer': 'SKengineer',
    'website': "https://www.skengineer.be/",
    'category': 'Purchase',
    'version': '17.1',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',

        'views/purchase_order_view.xml',

        'wizard/wizard_merge_purchase_order_view.xml',
    ],
    'images': [
        '/static/description/icon.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
