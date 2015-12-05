# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _name = 'fleet.vehicle'

    @api.multi
    def _get_avg_fuel_consumption(self):
        cr = self.env.cr
        for rec in self:
            cr.execute(""" SELECT MIN(od.value) as min, MAX(od.value) as max, SUM(fuel.liter) as lit
                            FROM fleet_vehicle_log_fuel fuel
                            JOIN fleet_vehicle_cost cost ON (fuel.cost_id = cost.id)
                            JOIN fleet_vehicle_odometer od ON (cost.odometer_id = od.id)
                            WHERE cost.vehicle_id = """ + str(rec.id))
            result = cr.fetchone() or ()
            cr.execute(""" SELECT last.lit
                            FROM (SELECT fuel.liter as lit
                                    FROM fleet_vehicle_log_fuel fuel
                                    JOIN fleet_vehicle_cost cost ON (fuel.cost_id = cost.id)
                                    WHERE cost.vehicle_id = """ + str(rec.id) + """
                                    ORDER BY fuel.id DESC
                                    LIMIT 1) last """)
            last_fuel = cr.fetchone() or ()
            if len(last_fuel) > 0 and len(result) > 0 and result[2] is not None and result[0] is not None and result[0] != result[1]:
                liter = result[2] - last_fuel[0]
                odo_max = result[1]
                odo_min = result[0]
                if odo_max - odo_min != 0:
                    avg = (liter / (odo_max - odo_min)) * 100
                else:
                    avg = 0
                rec.avg_fuel_consumption = avg
            else:
                rec.avg_fuel_consumption = 0

    @api.multi
    def _get_default_type(self):
        return self.env.ref('fleet_extend.fleet_vehicle_type_6')

    @api.multi
    @api.depends('mass', 'entire_mass')
    def _get_transport_capacity(self):
        for rec in self:
            transport_capacity = (rec.entire_mass or 0) - (rec.mass or 0)
            rec.transport_capacity = transport_capacity if (transport_capacity > 0 ) else 0
        return True

    @api.multi
    @api.depends('height', 'width', 'length')
    def _get_volume(self):
        for rec in self:
            vol = 0
            if rec.height and rec.width and rec.length:
                vol = rec.height * rec.width * rec.length
            rec.volume = vol

    type_id = fields.Many2one('fleet.vehicle.type', 'Vehicle type', default=_get_default_type)
    reg_required = fields.Boolean('Registration required?')
    avg_fuel_consumption = fields.Float(compute=_get_avg_fuel_consumption, string='Average fuel consumption')
    gps_num = fields.Char('GPS number', size=64)
    year_manufactured = fields.Char('Year of manufacturing')
    country_id = fields.Many2one('res.country', string='Country')
    engine_volume_ccm3 = fields.Integer('Engine volume in ccm3')
    engine_num = fields.Char('Engine number', size=64)
    mass = fields.Integer('Vehicle mass')
    entire_mass = fields.Integer('Entire mass')
    transport_capacity = fields.Integer(compute=_get_transport_capacity, string="Transport mass capacity",
                                        readonly=True)
    height = fields.Float('Height')
    width = fields.Float('Width')
    length = fields.Float('Length')
    volume = fields.Float('Volume', compute=_get_volume, store=True)

    #  tyre_ids': fields.many2many('fleet.vehicle.tyre','fleet_vehicle_tyre_rel', 'vehicle_id', 'tyre_id', string='Tires'),
    #  'gear_ids': fields.one2many( 'fleet.vehicle.gear.rel','vehicle_id', string='Gear'),
    # department_id = fields.Many2one('hr.department', string='Company department')
    #  contract_renewal_due_soon = fields.function(_get_contract_reminder_fnc, fnct_search=_search_contract_renewal_due_soon, type="boolean", string='Has Contracts to renew', multi='contract_info'),
    #          'contract_renewal_overdue': fields.function(_get_contract_reminder_fnc, fnct_search=_search_get_overdue_contract_reminder, type="boolean", string='Has Contracts Overdued', multi='contract_info'),
    #          'contract_renewal_name': fields.function(_get_contract_reminder_fnc, type="text", string='Name of contract to renew soon', multi='contract_info'),
    #          'contract_renewal_total': fields.function(_get_contract_reminder_fnc, type="integer", string='Total of contracts due or overdue minus one', multi='contract_info'),
    notes = fields.Text('Additional information')
    technical_inspection_date = fields.Date('Technical inspection date', default=False)
    six_months_technical_inspection = fields.Boolean('Every 6 months')
    #       'amortization_ids: fields.one2many('fleet.vehicle.amortization', 'vehicle_id', string='Amortization'),
    #             'amortization_factor': fields.float('Amortization factor', digits=(12,2)),
    #             'salvage_value': fields.float('Salvage value', digits=(12,2)),
    #     }

    @api.onchange('type_id')
    def onchange_type(self):
        for obj in self:
            if obj.type_id:
                obj.reg_required = obj.type_id.reg_required


