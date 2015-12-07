# -*- coding: utf-8 -*-

from openerp import models, api


class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    @api.multi
    def unlink(self):
        for obj in self:
            for child_cost in obj.generated_cost_ids:
                child_cost.sudo().unlink()
            if obj.cost_id:
                obj.cost_id.sudo().unlink()
        return super(FleetVehicleLogContract, self).unlink()

