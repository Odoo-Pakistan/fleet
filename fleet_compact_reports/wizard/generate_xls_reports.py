# -*- encoding: utf-8 -*-

import openpyxl
import base64
import cStringIO
from openerp import models, fields
from datetime import datetime



MONTHS = [(1, 'Januar'),
          (2, 'Februar'),
          (3, 'Mart'),
          (4, 'April'),
          (5, 'Maj'),
          (6, 'Jun'),
          (7, 'Jul'),
          (8, 'Avgust'),
          (9, 'Septembar'),
          (10, 'Octobar'),
          (11, 'Novembar'),
          (12, 'Decembar')]

YEARS = [(2015, '2015'),
         (2016, '2016'),
         (2017, '2017'),
         (2018, '2018'),
         (2019, '2019'),
         (2020, '2020')]

REPORT_TYPES = [
    ('obracun_plate', 'Obračun plate'),
    ('pregled_transporta_za_vozaca', 'Pregled transporta za vozača')
]

class FleetExcelReports(models.TransientModel):
    _name = 'fleet.compact.excel.report.selection'
    _description = 'Fleet excel report selection'

    def _reopen(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Report selection',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'res_model': 'fleet.compact.excel.report.selection',
                'target': 'new',
                }


    def _get_obracun_plate(self):
        wb = openpyxl.Workbook()
        ws = wb.create_sheet(0, self.employee_id.name)


        buf = cStringIO.StringIO()
        wb.save(buf)
        buf.seek(0)
        out = base64.encodestring(buf.read())
        buf.close()

        self.data = out
        self.name = "izvjestaj_plata_"+self.employee_id.name+"_"+dict(MONTHS).get(self.month)+"_"+dict(YEARS).get(self.year)
        self.state = 'get'
        return self._reopen()

    def _get_pregled_transporta_za_vozaca(self):
        # bitno je povaditi transporte u odredjenom vremenskom periodu
        wb = openpyxl.Workbook()
        ws = wb.create_sheet(0, self.employee_id.name)

        buf = cStringIO.StringIO()
        wb.save(buf)
        buf.seek(0)
        out = base64.encodestring(buf.read())
        buf.close()

        self.data = out
        self.name = "izvjestaj_transport_"+self.employee_id.name
        self.state = 'get'
        return self._reopen()


    name = fields.Char('File name', readonly=True)
    data = fields.Binary('File', readonly=True)
    report_type = fields.Selection(REPORT_TYPES, 'Odaberite željeni izvještaj', required=True)
    employee_id = fields.Many2one('hr.employee', 'Odaberite zaposlenog')
    date_start = fields.Date('Početni datum')
    date_stop = fields.Date('Krajnji datum')
    month = fields.Selection(MONTHS, 'Odaberite mjesec')
    year = fields.Selection(YEARS, 'Odaberite godinu')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    def get_report(self):
        if self.report_type == 'obracun_plate':
            self._get_obracun_plate()
        if self.report_type == 'pregled_transporta_za_vozaca':
            self._get_pregled_transporta_za_vozaca()














# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
