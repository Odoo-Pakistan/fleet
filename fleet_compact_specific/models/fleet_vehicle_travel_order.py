# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetVehicleTravelOrder(models.Model):
    _inherit = 'fleet.vehicle.travel.order'

    invoice_ids = fields.One2many('fleet.invoice', 'travel_order_id', string='Fakture')
