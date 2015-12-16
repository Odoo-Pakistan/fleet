# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    def _set_odometer(self):
        for rec in self:
            if not rec.odometer:
                raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
            value = rec.odometer
            if rec.odometer_id:
                rec.odometer_id.sudo().unlink()
            rec.odometer_id = self.env['fleet.vehicle.odometer'].create({'value':value, 'vehicle_id': rec.vehicle_id.id})

    @api.multi
    def _get_odometer(self):
        for record in self:
            if record.odometer_id:
                record.odometer = record.odometer_id.value


    odometer = fields.Float(string="Odometer Value", compute=_get_odometer, inverse=_set_odometer, help='Odometer measure of the vehicle at the moment of this log')
    department_id = fields.Many2one('hr.department', string='Department')
    notes = fields.Text('Additional info')

    # TODO: Ovdje treba napraviti nekakav nacin za obavjestavanje i racunanje ovih vrijednosti
    alert = fields.Boolean('Alert')
    next_service = fields.Float('Next Service', default=0.0)
    next_service_in = fields.Float('Next Service In', default=0.0)

    # @api.onchange('alert')
    # def on_change_subtype(self):
    #     self.next_service = 0.0
    #     if self.alert and self.cost_subtype_id:
    #         self.next_service = self.cost_subtype_id.next_service
    #         self.next_service_in = self.next_service + self.parent_id.odometer_id.value

    # @api.onchange('next_service')
    # def on_change_next_service(self):
    #     self.next_service_in = 0.0
    #     if self.alert and self.parent_id.odometer_id and self.next_service:
    #         self.next_service_in = self.next_service + self.parent_id.odometer_id.value
