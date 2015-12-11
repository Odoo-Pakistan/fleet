# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicleLogFuel(models.TransientModel):
    _name = 'fleet.config.settings'
    _inherit = 'res.config.settings'

    module_fleet_vehicle_cost_extend = fields.Boolean('Advanced vehicle cost features', help='This installs module fleet_vehicle_cost_extend')
    module_fleet_travel_order = fields.Boolean('Use travel orders', help='This installs module fleet_travel_order')
    module_fleet_travel_order_costs = fields.Boolean('Track costs via travel orders', help='This installs module fleet_travel_order_costs')
    module_fleet_travel_order_driver_cash = fields.Boolean('Track driver cash via travel order', help='This installs module fleet_travel_order_driver_cash')

    @api.one
    @api.onchange('module_fleet_travel_order_driver_cash')
    def change_travel_order_driver_cash(self):
        if self.module_fleet_travel_order_driver_cash:
            self.module_fleet_travel_order = True


    @api.one
    @api.onchange('module_fleet_travel_order_costs')
    def change_travel_order_costs(self):
        if self.module_fleet_travel_order_costs:
            self.module_fleet_travel_order = True
            self.module_fleet_vehicle_cost_extend = True
