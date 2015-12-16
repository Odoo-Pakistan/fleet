# -*- coding: utf-8 -*-

from openerp import models, fields, api

class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    @api.multi
    @api.depends('alert', 'next_service_relative', 'parent_id.odometer_id')
    def _compute_next_service_absolute(self):
        for rec in self:
            rec.next_service_absolute = 0.0
            if rec.alert and rec.parent_id.odometer_id and rec.next_service_relative:
                rec.next_service_absolute = rec.next_service_relative + rec.parent_id.odometer_id.value

#   TODO: Ovdje treba napraviti nekakav nacin za obavjestavanje i racunanje ovih vrijednosti
    alert = fields.Boolean('Alert')
    next_service_relative = fields.Float('Next Service', default=0.0)
    next_service_absolute = fields.Float(compute=_compute_next_service_absolute, string='Next Service Absolute', default=0.0)

    @api.onchange('alert', 'cost_subtype_id', 'parent_id.odometer_id')
    def on_change_subtype(self):
        self.next_service_relative = 0.0
        if self.alert and self.cost_subtype_id.next_service:
            self.next_service_relative = self.cost_subtype_id.next_service
            self.next_service_absolute = self.cost_subtype_id.next_service + (self.parent_id.odometer_id.value or 0)

    @api.one
    def make_done(self):
        self.alert = False
