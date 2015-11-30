# -*- encoding: utf-8 -*-

import openpyxl
import base64
import cStringIO
from openerp  import models,fields,api
from openerp.tools.translate import _
from datetime import datetime

REPORT_TYPES = [
    ('obracun_plate', 'Obračun plate'),
]


MONTHS = [(1,'Januar'),
          (2,'Februar'),
          (3,'Mart'),
          (4,'April'),
          (5,'Maj'),
          (6,'Jun'),
          (7,'Jul'),
          (8,'Avgust'),
          (9,'Septembar'),
          (10,'Octobar'),
          (11,'Novembar'),
          (12,'Decembar')]


class FleetExcelReports(models.TransientModel):

    _name = 'fleet.excel.report.selection'
    _description = 'Fleet excel report selection'

    report_type = fields.Selection(REPORT_TYPES, 'Odaberite željeni izvještaj', required=True)
    employee_id = fields.Many2one('hr.employee', 'Odaberite zaposlenog')
    date_start = fields.Date('Početni datum')
    date_stop = fields.Date('Krajnji datum')
    month = fields.Selection(MONTHS, 'Odaberite mjesec')

    def get_report(self):
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: