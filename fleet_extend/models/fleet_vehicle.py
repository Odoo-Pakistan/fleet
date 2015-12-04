from openerp  import models,fields,api



class fleet_vehicle(models.Model):
    
    _inherit = 'fleet.vehicle'
    _name = 'fleet.vehicle'
    
    
    @api.multi
    def _get_avg_fuel_consumption(self):
        pass
    
    @api.multi
    def _get_default_type(self):
        pass
    
    @api.multi
    def _get_transport_capacity(self):
        pass
    
    
    @api.multi
    @api.depends('height', 'width', 'length')
    def _get_volume(self):
        for rec in self:
            vol = 0
            if rec.height and rec.width and rec.length:
                vol = rec.height * rec.width * rec.length
            rec.volume = vol
    
    
    
    type_id = fields.Many2one('fleet.vehicle.type', 'Vehicle type',default=_get_default_type)
    reg_required = fields.Boolean('Registration required?')
    avg_fuel_consumption = fields.Float(compute = _get_avg_fuel_consumption, string='Average fuel consumption')
    gps_num = fields.Char('GPS number', size=64)
    year_manufactured = fields.Char('Year of manufacturing')
    country_id = fields.Many2one('res.country', string='Country')
    engine_volume_ccm3 = fields.Integer('Engine volume in ccm3')
    engine_num = fields.Char('Engine number', size=64)
    mass = fields.Integer('Vehicle mass')
    entire_mass = fields.Integer('Entire mass')
    transport_capacity = fields.Integer(compute= _get_transport_capacity, string="Transport mass capacity", readonly=True)
#    tyre_ids': fields.many2many('fleet.vehicle.tyre','fleet_vehicle_tyre_rel', 'vehicle_id', 'tyre_id', string='Tires'),
#    'gear_ids': fields.one2many( 'fleet.vehicle.gear.rel','vehicle_id', string='Gear'),
#   department_id = fields.Many2one('hr.department', string='Company department')
#    contract_renewal_due_soon = fields.function(_get_contract_reminder_fnc, fnct_search=_search_contract_renewal_due_soon, type="boolean", string='Has Contracts to renew', multi='contract_info'),
#            'contract_renewal_overdue': fields.function(_get_contract_reminder_fnc, fnct_search=_search_get_overdue_contract_reminder, type="boolean", string='Has Contracts Overdued', multi='contract_info'),
#            'contract_renewal_name': fields.function(_get_contract_reminder_fnc, type="text", string='Name of contract to renew soon', multi='contract_info'),
#            'contract_renewal_total': fields.function(_get_contract_reminder_fnc, type="integer", string='Total of contracts due or overdue minus one', multi='contract_info'),
    notes = fields.Text('Additional information')
    technical_inspection_date = fields.Date('Technical inspection date',default=False)
    six_months_technical_inspection = fields.Boolean('Every 6 months')
#       'amortization_ids: fields.one2many('fleet.vehicle.amortization', 'vehicle_id', string='Amortization'),
#             'amortization_factor': fields.float('Amortization factor', digits=(12,2)),
#             'salvage_value': fields.float('Salvage value', digits=(12,2)),
#             'travel_order_ids': fields.one2many('fleet.vehicle.travel.order', 'vehicle_id', 'Travel Orders'),
#             'travel_order_count': fields.function(_count_travel_orders, type='integer', string='Travel Orders'),
#     }


    #sa v8
    height = fields.Float('Height')
    width = fields.Float('Width')
    length = fields.Float('Length')
    volume = fields.Float('Volume', compute=_get_volume, store=True)
    

    @api.onchange('type_id')
    def onchange_type(self):
        pass
#     @api.v7
#     def onchange_type(self, cr, user, ids, type_id, context={}):
#         model = self.pool.get('fleet.vehicle.type')
#         obj = model.read(cr, user, type_id, ['reg_required'])
#         if obj:
#             reg_required = obj.get('reg_required', False)
#             return {
#                 'value': {'reg_required': reg_required}
#                 }
#         else:
#             return True
#     


   