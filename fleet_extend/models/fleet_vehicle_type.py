from openerp  import models,fields,api


class fleet_vechile_type(models.Model):
    
    _name = 'fleet.vehicle.type'
    _description = 'Fleet vehicle type'  
    
    name = fields.Char('Name', size=128, required=True)
    reg_required = fields.Boolean('Registration required?')
    measure = fields.Selection([('km','Kilometers'),('hour','Working hours')],'Measure unit')
    vehicle_ids = fields.One2many('fleet.vehicle', 'type_id', 'Vehicles')
    