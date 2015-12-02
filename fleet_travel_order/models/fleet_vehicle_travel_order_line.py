from openerp  import models,fields,api



class fleet_vehicle_travel_order_line(models.Model):
    
    _name='fleet.vehicle.travel.order.line'
    
    def _get_start_odometer(self):
        pass
    
    def _set_start_odometer(self):
        pass
    
    def _get_stop_odometer(self):
        pass
    
    def _set_stop_odometer(self):
        pass
    
    
    
    #columns
    date = fields.Date('Date')
    distance = fields.Char('Distance')
    travel_order_id = fields.Many2one('fleet.vehicle.travel.order',string = 'Travel Order')
    start_odometer_id = fields.Many2one('fleet.vehicle.odometer', string ='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    start_odometer = fields.Float(compute=_get_start_odometer, inverse = _set_start_odometer, string='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer_id = fields.Many2one('fleet.vehicle.odometer', string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer = fields.Float(compute=_get_stop_odometer, inverse = _set_stop_odometer, string = 'Odometer stop', help='Odometer measure of the vehicle at the moment of this log')