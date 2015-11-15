# -*- coding: utf-8 -*-
##############################################################################
# Created by Khin Aye Mon on 11/15/15.
# @kankaungmalay
# Copyright (c) 2015. All rights reserved.
##############################################################################
from openerp.osv import fields, osv
from openerp import api, _

import logging
_logger = logging.getLogger(__name__)

class DeliveryOrderWizard(osv.TransientModel):
    _name = 'delivery.order.report.wiz'

    @api.multi
    def print_report(self):
        doc_ids = self.env['stock.picking'].search([], order="id ASC")

        data = {}
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]

        res = self.env['report'].get_action(doc_ids,
        'delivery_order_report.report_delivery_order_pdf', data=data)
        return res

    _columns = {
        'company_id': fields.many2one('res.company', string='Company'),
        'date_from': fields.date(string='Start Date', required=True),
        'date_to': fields.date(string='End Date', required=True),
    }

    _defaults = {
    }
