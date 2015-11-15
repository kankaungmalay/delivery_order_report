# -*- coding: utf-8 -*-
##############################################################################
# Created by Khin Aye Mon on 11/15/15.
# @kankaungmalay
# Copyright (c) 2015. All rights reserved.
##############################################################################
from datetime import datetime
from openerp import models, api
from openerp.report import report_sxw
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class DeliveryOrderReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(DeliveryOrderReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'display_company': self.display_company,
            'has_orders': self.has_orders,
            'get_order_lines': self.get_order_lines,
            'get_date_from': self.get_date_from,
            'get_date_to': self.get_date_to,
        })
############################Read Data#######################################
    def _get_info(self, data, field, model):
        info = data.get('form', {}).get(field)
        if info:
            if self.pool.get(model).browse(self.cr, self.uid, info[0]):
                return self.pool.get(model).browse(self.cr, self.uid, info[0])
        return False

    def _get_form_param(self, param, data, default = False):
        return data.get('form', {}).get(param, default)

############################Report Functions################################
    def get_date_from(self, data):
            return self._get_form_param('date_from', data)

    def get_date_to(self, data):
        return self._get_form_param('date_to', data)

    def get_company_ids(self, data):
        return self._get_info(data, 'company_id', 'res.company')

    def get_company(self, data):
        return self._get_form_param('company_id', data)

    def get_search_criteria(self, data):
        company_ids = []

        date_from = self.get_date_from(data)#Filter type date
        date_to = self.get_date_to(data)#Filter type date

        company_list = self.get_company_ids(data)#Filter Company
        if company_list:
            for company in company_list:
                company_ids.append(company.id)
        else:
            company_ids = self.pool.get('res.company').search(self.cr, self.uid, [])

        return date_from, date_to, company_ids

##############################Display Data##################################
    def display_company(self, data):
        name = ''
        if not self.get_company_ids(data):
            return _('All Companies')
        else:
            companies = self.get_company_ids(data)
            for company in companies:
               name += company.name + ' , '
            return name[:-2]

    def has_orders(self, data):
        lines_obj = self.get_orders(data)
        if lines_obj:
            return True
        return False

    def get_stock_picking_type_ids(self):
        stock_picking_type_obj = self.pool.get('stock.picking.type')
        return stock_picking_type_obj.search(self.cr, self.uid, [('code', 'ilike', '%outgoing%')])

    def get_orders(self, data):
        stock_picking_obj = self.pool.get('stock.picking')
        date_from, date_to, company_ids = self.get_search_criteria(data)

        date_from = datetime.strptime(date_from, "%Y-%m-%d").date().strftime('%Y-%m-%d 00:00:00')
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date().strftime('%Y-%m-%d 23:59:59')
        sp_domain = [
            ('state', 'in', ['done', 'assigned']),
            ('company_id', 'in', company_ids),
            ('min_date', '>=', date_from),
            ('min_date', '<=', date_to),
            ('picking_type_id', 'in', self.get_stock_picking_type_ids())
        ]
        sp_ids = stock_picking_obj.search(self.cr, self.uid, sp_domain)
        order_obj = stock_picking_obj.browse(self.cr, self.uid, sp_ids)
        return order_obj

    def get_order_lines(self, data):
        orders = []
        lines_obj = self.get_orders(data)
        for line in lines_obj:
            line_report = {}
            line_report['scheduled_date'] = line.min_date
            line_report['created_date'] = line.date
            line_report['customer'] = line.partner_id.name
            line_report['so_no'] = line.origin
            line_report['do_no'] = line.name
            line_report['transferred_date'] = line.date_done
            if line.state == 'done':
                line_report['status'] = 'Transferred'
            elif line.state == 'assigned':
                line_report['status'] = 'Ready to Transfer'
            orders.append(line_report)
        orders = sorted(orders, key = lambda d: (d['scheduled_date'], d['customer']))
        return orders

class report_delivery_order_pdf(models.AbstractModel):
    _name = 'report.delivery_order_report.report_delivery_order_pdf'
    _inherit = 'report.abstract_report'
    _template = 'delivery_order_report.report_delivery_order_pdf'
    _wrapped_report_class = DeliveryOrderReport