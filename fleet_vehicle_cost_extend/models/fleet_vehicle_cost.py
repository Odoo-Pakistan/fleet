# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    @api.multi
    def _set_odometer(self):
        for rec in self:
            if not rec.odometer:
                raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
            value = rec.odometer
            if rec.odometer_id:
                rec.odometer_id.write({'value':value,'date':rec.date})
            else:
                rec.odometer_id = self.env['fleet.vehicle.odometer'].create({'value':value, 'vehicle_id': rec.vehicle_id.id,'date':rec.date})

    @api.multi
    def _get_odometer(self):
        for record in self:
            if record.odometer_id:
                record.odometer = record.odometer_id.value


    odometer = fields.Float(string="Odometer Value", compute=_get_odometer, inverse=_set_odometer, help='Odometer measure of the vehicle at the moment of this log')
    department_id = fields.Many2one('hr.department', string='Department')
    notes = fields.Text('Additional info')
