# -*- coding: utf-8 -*-
##############################################################################
# Created by Khin Aye Mon on 11/15/15.
# @kankaungmalay
# Copyright (c) 2015. All rights reserved.
##############################################################################
{
    'name': 'Delivery Order Report',
    'version': '1.0',
    "author": 'KhinAyeMon',
    'category': 'Warehouse Management',
    'description': """
Delivery Order Report
====================    
This module will add Delivery Order Report under Warehouse/Traceability/
""",
    'depends': [
        'stock', 'product',
    ],
    'data': [
        'delivery_order_report.xml',
        'views/report_delivery_order_pdf.xml',
        'wizard/delivery_order_report_wizard.xml',
    ],
    'installable': True,
    'active': False,
}
