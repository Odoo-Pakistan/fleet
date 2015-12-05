# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    travel_order_id = fields.Many2one('fleet.vehicle.travel.order', string='Travel Order')
