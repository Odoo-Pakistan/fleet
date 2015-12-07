# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    is_deposited = fields.Boolean('Is contract deposited?')
