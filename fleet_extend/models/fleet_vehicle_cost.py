# -*- coding: utf-8 -*-

from openerp import models, api


class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    @api.multi
    def unlink(self):
        for obj in self:
            if obj.odometer_id:
                obj.odometer_id.sudo().unlink()
        return super(FleetVehicleCost, self).unlink()