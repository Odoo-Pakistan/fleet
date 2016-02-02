from openerp  import models,fields,api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class fleet_vehicle_travel_order_line(models.Model):

    _name='fleet.vehicle.travel.order.line'



    def _check_odometer_validity(self,check_type):
    #provjerava da li je start veci od stop vrijednosti i suprotno
    #ako je check_type = start onda je pozvana iz start odometra
        if(check_type == 'start'):
            if not self.stop_odometer_id:
                return True
            if self.start_odometer > self.stop_odometer_id.value:
                return False
            else:
                return True
        else:
            if not self.start_odometer_id:
                return True
            if self.stop_odometer < self.start_odometer_id.value:
                return False
            else:
                return True



    def _set_start_odometer(self):
        for obj in self:
            if not obj.start_odometer:
                raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
            if not obj._check_odometer_validity('start'):
                raise except_orm(_('Odometer error'),_('Start odometer value must not be bigger than stop odometer value'))
            value = obj.start_odometer
            if obj.start_odometer_id:
                obj.start_odometer_id.write({'value':value,'date':obj.date})
            else:
                obj.start_odometer_id = self.env['fleet.vehicle.odometer'].create({'value':value,'vehicle_id':obj.travel_order_id.vehicle_id.id,'date':obj.date})


    def _set_stop_odometer(self):
        for obj in self:
            if not obj.stop_odometer:
                raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
            if not obj._check_odometer_validity('stop'):
                raise except_orm(_('Odometer error'),_('Stop odometer value must not be lower than start odometer value'))
            value = obj.stop_odometer
            if obj.stop_odometer_id:
                obj.stop_odometer_id.write({'value':value,'date':obj.date})
            else:
                obj.stop_odometer_id = self.env['fleet.vehicle.odometer'].create({'value':value,'vehicle_id':obj.travel_order_id.vehicle_id.id,'date':obj.date})

    def _get_start_odometer(self):
        for obj in self:
            if obj.start_odometer_id:
                obj.start_odometer = obj.start_odometer_id.value
            else:
                obj.start_odometer = 0

    def _get_stop_odometer(self):
        for obj in self:
            if obj.stop_odometer_id:
                obj.stop_odometer = obj.stop_odometer_id.value
            else:
                obj.stop_odometer = 0

    #columns
    date = fields.Date('Date')
    distance = fields.Char('Distance')
    travel_order_id = fields.Many2one('fleet.vehicle.travel.order',string = 'Travel Order',ondelete="cascade")
    start_odometer_id = fields.Many2one('fleet.vehicle.odometer', string ='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    start_odometer = fields.Float(compute=_get_start_odometer, inverse = _set_start_odometer, string='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer_id = fields.Many2one('fleet.vehicle.odometer', string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer = fields.Float(compute=_get_stop_odometer, inverse = _set_stop_odometer, string = 'Odometer stop', help='Odometer measure of the vehicle at the moment of this log')


    @api.v7
    def create(self, cr, uid, data, context=None):
    #ako nisu setovani da se ne bi pozivala funckija za setovanje
        if 'start_odometer' in data and not data['start_odometer']:
            del(data['start_odometer'])
        if 'stop_odometer' in data and not data['stop_odometer']:
            del(data['stop_odometer'])
        return super(fleet_vehicle_travel_order_line, self).create(cr, uid, data, context=context)



    @api.v7
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            start_id = this_obj.start_odometer_id
            stop_id = this_obj.stop_odometer_id
            if (start_id):
                self.pool.get('fleet.vehicle.odometer').unlink(cr,1,start_id.id)
            if (stop_id):
                self.pool.get('fleet.vehicle.odometer').unlink(cr,1,stop_id.id)
        return super(fleet_vehicle_travel_order_line,self).unlink(cr,uid,ids,context=context)