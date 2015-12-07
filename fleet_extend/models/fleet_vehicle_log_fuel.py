# -*- coding: utf-8 -*-

from openerp import models


class FleetVehicleLogFuel(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'

    def unlink(self, cr, uid, ids, context=None):
        this_objs = self.browse(cr, uid, ids, context=context)
        for this_obj in this_objs:
            if this_obj.cost_id:
                self.pool.get('fleet.vehicle.cost').unlink(cr, 1, this_obj.cost_id.id)
        return super(FleetVehicleLogFuel, self).unlink(cr, uid, ids, context=context)
