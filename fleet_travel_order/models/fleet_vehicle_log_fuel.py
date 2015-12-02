from openerp  import models,fields,api




class fleet_vehicle_log_fuel(models.Model):
    
    _name='fleet.vehicle.log.fuel'
    _inherit='fleet.vehicle.log.fuel'
     
    travel_order_id = fields.Many2one('fleet.vehicle.travel.order',string='Travel order') 
#     department_id = fields.Related('vehicle_id', 'department_id',store=True, relation='hr.department', type='many2one', string='Department'),
 
    @api.v7
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if(this_obj.cost_id):
                self.pool.get('fleet.vehicle.cost').unlink(cr,1,this_obj.cost_id.id)
        return super(fleet_vehicle_log_fuel,self).unlink(cr,uid,ids,context=context)