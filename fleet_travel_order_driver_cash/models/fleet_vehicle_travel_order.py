from openerp import models,api,fields



class FleetVehicleTravelOrder(models.Model):
    
    _inherit="fleet.vehicle.travel.order"
    _name="fleet.vehicle.travel.order"
    
    
    driver_cash_ids = fields.One2many('fleet.travel.order.driver.cash','travel_order_id',string='Driver cash')