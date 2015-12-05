from openerp  import models,fields,api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
import time


# class fleet_vehicle_cost(models.Model):
#     _name = 'fleet.vehicle.cost'
#     _inherit='fleet.vehicle.cost'
#
#     travel_order_id = fields.Many2one('fleet.vehicle.travel.order',string = 'Travel Order')
#     additional_info = fields.Text('Info')
#
#     alert = fields.Boolean('Alert')
#     next_service = fields.Float('Next Service', default=0.0)
#     next_service_in = fields.Float('Next Service In', default=0.0)
#
#
#
#
#
#     @api.onchange('alert')
#     def on_change_subtype(self):
#         self.next_service = 0.0
#         if self.alert and self.cost_subtype_id:
#             self.next_service = self.cost_subtype_id.next_service
#             self.next_service_in = self.next_service + self.parent_id.odometer_id.value
#
#
#
#     @api.onchange('next_service')
#     def on_change_next_service(self):
#         self.next_service_in = 0.0
#         if self.alert and self.parent_id.odometer_id and self.next_service:
#             self.next_service_in = self.next_service + self.parent_id.odometer_id.value



# class fleet_vehicle_log_services(models.Model):
#     _name = 'fleet.vehicle.log.services'
#     _inherit='fleet.vehicle.log.services'
#
#     @api.depends('cost_ids.amount')
#     def _get_tmp_amount(self):
#         for rec in self:
#             amm = 0
#             if rec.cost_ids:
#                 for line in rec.cost_ids:
#                     amm += line.amount
#                 if rec.amount != amm:
#                     self.write({'amount': amm})
#                 rec.tmp_amount = amm
#
#     @api.multi
#     def _has_alerts(self):
#         for rec in self:
#             odometer = rec.odometer
#             vehicle_odometer = rec.vehicle_id.odometer
#             for line in rec.cost_ids:
#                 if line.alert:
#                     diff = (odometer+line.next_service) - (vehicle_odometer)
#                     if diff < 10000.0:
#                         rec.has_alerts = True
#
#
#     def _search_alerts(self, operator, value):
#         assert operator in ('=', '!=', '<>') and value in (True, False), _('Operation not supported')
#         res_ids=[]
#         if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
#             search_operator = 'in'
#         else:
#             search_operator = 'not in'
#         for rec in self.search([]):
#             if rec.has_alerts:
#                 res_ids.append(rec.id)
#         return [('id', search_operator, res_ids)]
#
#     tmp_amount = fields.Float('TMP_AMM', compute=_get_tmp_amount)
#     has_alerts = fields.Boolean('Has Alerts', compute=_has_alerts, search=_search_alerts)




# class fleet_service_type(models.Model):
#     _name='fleet.service.type'
#     _inherit='fleet.service.type'
#
#     category = fields.Selection([('contract', 'Contract'), ('service', 'Service'), ('both', 'Both'),('fuel', 'Fuel'), ('other','Other')], string = 'Category', required=True, help='Choose wheter the service refer to contracts, vehicle services or both')
#     parent_id = fields.Many2one('fleet.service.type', string='Parent')
#     next_service = fields.Float('Next service', default=0.0)



# class fleet_vehicle_log_other_cost(models.Model):
#
#     _name = 'fleet.vehicle.log.other.cost'
#     _description = 'Other costs for vehicles'
#     _inherits = {'fleet.vehicle.cost':'cost_id'}
#
#
#     name = fields.Char('Name')
#     cost_id = fields.Many2one('fleet.vehicle.cost',string="Cost",required=True,ondelete='cascade')
#     purchaser_id = fields.Many2one('res.partner',string='Purchaser',domain="[('employee','=',True)]")
#     vendor_id = fields.Many2one('res.partner',string='Supplier', domain="[('supplier','=',True)]")
#     inv_ref = fields.Char(string='Invoice Reference')
# #     cost_amount = fields.Float (related='cost_id.amount',string='Amount',store=True)
#
#     @api.multi
#     def unlink(self):
#         for obj in self:
#             if obj.cost_id:
#                 obj.cost_id.unlink()
#         return super(fleet_vehicle_log_other_cost, self).unlink()
#
#     #napraviti oncahnge za vehicle_id...koja popunjava odometer

# class fleet_vehicle(models.Model):
#     _name = 'fleet.vehicle'
#     _inherit = 'fleet.vehicle'
#
#     @api.multi
#     @api.depends('height', 'width', 'length')
#     def _get_volume(self):
#         for rec in self:
#             vol = 0
#             if rec.height and rec.width and rec.length:
#                 vol = rec.height * rec.width * rec.length
#             rec.volume = vol
#
#     height = fields.Float('Height')
#     width = fields.Float('Width')
#     length = fields.Float('Length')
#     volume = fields.Float('Volume', compute=_get_volume, store=True)

class fleet_vehicle_travel_order_cargo_value_line(models.Model):
    _name = 'fleet.vehicle.travel.order.cargo.value.line'

    @api.multi
    @api.depends('travel_order_id.date', 'travel_order_id.driver1_id')
    def _compute_additional_info(self):
        for rec in self:
            if (rec.travel_order_id.date):
                rec.date = rec.travel_order_id.date
                rec.year = str(time.strptime(rec.date, DEFAULT_SERVER_DATE_FORMAT).tm_year)
            if (rec.travel_order_id.driver1_id):
                rec.employee_id = rec.travel_order_id.driver1_id


    date = fields.Date('Date', compute=_compute_additional_info, store=True)
    year = fields.Char('Year', compute=_compute_additional_info, store=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', compute=_compute_additional_info, store=True)

    travel_order_id = fields.Many2one('fleet.vehicle.travel.order', 'Travel Order')
    partner_id = fields.Many2one('res.partner', 'Partner')
    value = fields.Float('Value')
    notes = fields.Text('Notes')

class fleet_vehicle_travel_order(models.Model):

    _name= 'fleet.vehicle.travel.order'
    _inherit = 'fleet.vehicle.travel.order'



    # @api.multi
    # def _compute_costs(self):
    #     if len(self) == 1:
    #         self.env.cr.execute("""SELECT pn.id,(SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'services' AND travel_order_id = pn.id) as Servis,
    #                                          (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'fuel' AND travel_order_id = pn.id) as Fuel,
    #                                          (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'other' AND travel_order_id = pn.id) as Other
    #                             FROM fleet_vehicle_travel_order as pn
    #                             WHERE pn.id = """+str(self[0].id))
    #         result = self.env.cr.fetchone();
    #         if(result[1]):
    #             service_cost = result[1]
    #         else:
    #             service_cost = 0
    #         if(result[2]):
    #             fuel_cost = result[2]
    #         else:
    #             fuel_cost = 0
    #         if(result[3]):
    #             other_cost = result[3]
    #         else:
    #             other_cost = 0
    #
    #         self[0].total_service_cost = service_cost
    #         self[0].total_fuel_cost = fuel_cost
    #         self[0].total_other_cost = other_cost
    #         self[0].total_costs =  service_cost + fuel_cost + other_cost
    #     else:
    #         self.env.cr.execute("""SELECT pn.id,(SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'services' AND travel_order_id = pn.id) as Servis,
    #                                         (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'fuel' AND travel_order_id = pn.id) as Fuel,
    #                                         (SELECT SUM(amount) FROM fleet_vehicle_cost WHERE cost_type = 'other' AND travel_order_id = pn.id) as Other
    #                                FROM fleet_vehicle_travel_order as pn""")
    #         result_set = self.env.cr.fetchall();
    #
    #         for tuple in result_set:
    #             if(tuple[1]):
    #                 service_cost = tuple[1]
    #             else:
    #                 service_cost = 0
    #             if(tuple[2]):
    #                 fuel_cost = tuple[2]
    #             else:
    #                 fuel_cost = 0
    #             if(tuple[3]):
    #                 other_cost = tuple[3]
    #             else:
    #                 other_cost = 0
    #
    #
    #             pn = self.search([('id','=',tuple[0])])
    #             pn.total_service_cost = service_cost
    #             pn.total_fuel_cost = fuel_cost
    #             pn.total_other_cost = other_cost
    #             pn.total_costs = service_cost + fuel_cost + other_cost


    # @api.multi
    # def _compute_total_km(self):
    #     for rec in self:
    #         rec.total_km = 0.0
    #         if rec.start_odometer_id and rec.stop_odometer_id:
    #             rec.total_km = rec.stop_odometer_id.value - rec.start_odometer_id.value


    @api.multi
    @api.depends('cargo_value_line_ids.value', 'total_fuel_cost', 'total_other_cost')
    def _compute_profit(self):
        for rec in self:
            total_cargo_value = 0.0
            for line in self.cargo_value_line_ids:
                total_cargo_value += line.value
            rec.profit = total_cargo_value - rec.total_fuel_cost - rec.total_other_cost






    # @api.multi
    # def _get_counts_for_travel_order(self):
    #     for obj in self:
    #         self.services_count = self.env['fleet.vehicle.log.services'].search_count([('travel_order_id','=',self.id)])
    #         self.other_cost_count = self.env['fleet.vehicle.log.other.cost'].search_count([('travel_order_id','=',self.id)])





    # private_km = fields.Float(string='Private (km)')
    # loaded_km = fields.Float(string='Loaded (km)')
    # total_km = fields.Float(string='Total (km)', compute=_compute_total_km)
    # cost_ids = fields.One2many('fleet.vehicle.cost','travel_order_id',string="Costs")
    # services_count = fields.Integer(compute=_get_counts_for_travel_order,string='Services')
    # other_cost_count = fields.Integer(compute=_get_counts_for_travel_order,string='Other Costs')


    driver_cash = fields.Float('Driver Cash')

    # total_fuel_cost =fields.Float(string = 'Fuel costs',compute=_compute_costs)
    # total_service_cost = fields.Float(string = 'Service costs',compute=_compute_costs)
    # total_other_cost = fields.Float(string = 'Other costs',compute=_compute_costs)
    # total_costs = fields.Float(string='Total costs',compute=_compute_costs)

    profit = fields.Float('Profit', compute=_compute_profit)


    cargo_value_line_ids = fields.One2many('fleet.vehicle.travel.order.cargo.value.line', 'travel_order_id', 'Cargo Value')





    # @api.multi
    # def return_services(self):
    #
    #     return  {
    #                 "type": "ir.actions.act_window",
    #                 "res_model": "fleet.vehicle.log.services",
    #                 "views": [[False, "tree"], [False, "form"]],
    #                 "domain": [["travel_order_id", "=", self[0].id]],
    #                 "context": {'default_travel_order_id':self[0].id,'default_vehicle_id':self[0].vehicle_id.id}
    #             }

    # @api.multi
    # def return_other_costs(self):
    #
    #     return  {
    #                 "type": "ir.actions.act_window",
    #                 "res_model": "fleet.vehicle.log.other.cost",
    #                 "views": [[False, "tree"], [False, "form"]],
    #                 "domain": [["travel_order_id", "=", self[0].id]],
    #                 "context": {'default_travel_order_id':self[0].id,'default_vehicle_id':self[0].vehicle_id.id}
    #             }

    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #
    #     remove_fields = ('total_fuel_cost','total_service_cost','total_other_cost','total_costs')
    #     keep_fields = [f for f in fields  if not f in remove_fields]
    #     _super = super(fleet_vehicle_travel_order, self)
    #     return _super.read_group(domain, keep_fields, groupby=groupby,offset=offset, limit=limit,orderby=orderby,lazy=lazy)






