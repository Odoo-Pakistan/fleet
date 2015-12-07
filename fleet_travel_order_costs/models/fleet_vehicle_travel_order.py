# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicleTravelOrder(models.Model):
    _inherit = 'fleet.vehicle.travel.order'

    @api.multi
    def _compute_costs(self):
        if len(self) == 1:
            self.env.cr.execute("""SELECT pn.id,(SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'services' AND travel_order_id = pn.id) as Servis,
                                             (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'fuel' AND travel_order_id = pn.id) as Fuel,
                                             (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'other' AND travel_order_id = pn.id) as Other
                                FROM fleet_vehicle_travel_order as pn
                                WHERE pn.id = """+str(self[0].id))
            result = self.env.cr.fetchone();
            if(result[1]):
                service_cost = result[1]
            else:
                service_cost = 0
            if(result[2]):
                fuel_cost = result[2]
            else:
                fuel_cost = 0
            if(result[3]):
                other_cost = result[3]
            else:
                other_cost = 0

            self[0].total_service_cost = service_cost
            self[0].total_fuel_cost = fuel_cost
            self[0].total_other_cost = other_cost
            self[0].total_costs =  service_cost + fuel_cost + other_cost
        else:
            self.env.cr.execute("""SELECT pn.id,(SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'services' AND travel_order_id = pn.id) as Servis,
                                            (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'fuel' AND travel_order_id = pn.id) as Fuel,
                                            (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'other' AND travel_order_id = pn.id) as Other
                                   FROM fleet_vehicle_travel_order as pn""")
            result_set = self.env.cr.fetchall();

            for tuple in result_set:
                if(tuple[1]):
                    service_cost = tuple[1]
                else:
                    service_cost = 0
                if(tuple[2]):
                    fuel_cost = tuple[2]
                else:
                    fuel_cost = 0
                if(tuple[3]):
                    other_cost = tuple[3]
                else:
                    other_cost = 0


                pn = self.search([('id','=',tuple[0])])
                pn.total_service_cost = service_cost
                pn.total_fuel_cost = fuel_cost
                pn.total_other_cost = other_cost
                pn.total_costs = service_cost + fuel_cost + other_cost

    @api.multi
    def _get_counts_for_travel_order(self):
        for obj in self:
            self.services_count = self.env['fleet.vehicle.log.services'].search_count(
                [('travel_order_id', '=', obj.id)])
            self.other_cost_count = self.env['fleet.vehicle.log.other.cost'].search_count(
                [('travel_order_id', '=', obj.id)])

    total_fuel_cost = fields.Float(string='Fuel costs', compute=_compute_costs)
    total_service_cost = fields.Float(string='Service costs', compute=_compute_costs)
    total_other_cost = fields.Float(string='Other costs', compute=_compute_costs)
    total_costs = fields.Float(string='Total costs', compute=_compute_costs)

    cost_ids = fields.One2many('fleet.vehicle.cost', 'travel_order_id', string="Costs")
    services_count = fields.Integer(compute=_get_counts_for_travel_order, string='Services')
    other_cost_count = fields.Integer(compute=_get_counts_for_travel_order, string='Other Costs')

    @api.multi
    def return_services(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "fleet.vehicle.log.services",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["travel_order_id", "=", self[0].id]],
            "context": {'default_travel_order_id': self[0].id, 'default_vehicle_id': self[0].vehicle_id.id}
        }

    @api.multi
    def return_other_costs(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "fleet.vehicle.log.other.cost",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["travel_order_id", "=", self[0].id]],
            "context": {'default_travel_order_id': self[0].id, 'default_vehicle_id': self[0].vehicle_id.id}
        }

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        remove_fields = ('total_fuel_cost','total_service_cost','total_other_cost','total_costs')
        keep_fields = [f for f in fields  if not f in remove_fields]
        _super = super(FleetVehicleTravelOrder, self)
        return _super.read_group(domain, keep_fields, groupby=groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
