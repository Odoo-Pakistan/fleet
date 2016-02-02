from openerp  import models,fields,api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
import time


class fleet_vehicle_travel_order(models.Model):

    _name = 'fleet.vehicle.travel.order'
    _rec_name = 'series'

    @api.multi
    def _get_fuel_log_count(self):
        for obj in self:
            obj.fuel_log_count = len(obj.fuel_log_ids)

    @api.multi
    @api.depends('travel_order_line_ids.start_odometer_id', 'travel_order_line_ids.stop_odometer_id')
    def _get_odometer(self):
        for obj in self:
            if obj.travel_order_line_ids and obj.travel_order_line_ids[0]:
                obj.start_odometer = obj.travel_order_line_ids[0].start_odometer
                obj.stop_odometer = obj.travel_order_line_ids[len(obj.travel_order_line_ids)-1].stop_odometer
                obj.total_km = obj.stop_odometer - obj.start_odometer
            else:
                obj.start_odometer = 0
                obj.stop_odometer = 0
                obj.total_km = 0

    #columns
    vehicle_id = fields.Many2one('fleet.vehicle','Vehicle',required=True)
    additional_vehicle_id = fields.Many2one('fleet.vehicle','Additional vehicle')
    place = fields.Char('Place',size=64,default='Banja Luka')
    date = fields.Date('Date',required = True,default=fields.datetime.now())
    num = fields.Char('Number',size=64,required = True)
    type = fields.Selection([('cargo','PN3'),('passenger','PN4')],'Type',default='cargo')
    driver1_id = fields.Many2one('hr.employee','1st Driver',required=True)
    driver2_id = fields.Many2one('hr.employee','2nd Driver')
    codriver1_id = fields.Many2one('hr.employee','1st Co-Driver')
    codriver2_id = fields.Many2one('hr.employee','2nd Co-Driver')
    codriver3_id = fields.Many2one('hr.employee','3rd Co-Driver')
    codriver4_id = fields.Many2one('hr.employee','4th Co-Driver')
    cargo_worker1_id = fields.Many2one('hr.employee','1st Cargo Worker')
    cargo_worker2_id = fields.Many2one('hr.employee','2nd Cargo Worker')
    cargo_worker3_id = fields.Many2one('hr.employee','3rd Cargo Worker')
    cargo_worker4_id = fields.Many2one('hr.employee','4th Cargo Worker')
    distance = fields.Char('Distance',size=256)
    fuel_log_ids = fields.One2many('fleet.vehicle.log.fuel','travel_order_id')
    fuel_log_count = fields.Integer(compute=_get_fuel_log_count,string='Fuel Logs')
    travel_order_line_ids = fields.One2many('fleet.vehicle.travel.order.line','travel_order_id')
    series = fields.Char('Series',size=64)
    start_odometer_id = fields.Many2one('fleet.vehicle.odometer', string ='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    start_odometer = fields.Float(compute=_get_odometer, readonly=True, string='Odometer start', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer_id = fields.Many2one('fleet.vehicle.odometer', string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log')
    stop_odometer = fields.Float(compute=_get_odometer, readonly=True, string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log')
    #sa V8
    private_km = fields.Float(string='Private (km)')
    loaded_km = fields.Float(string='Loaded (km)')
    total_km = fields.Float(string='Total (km)', compute=_get_odometer, store=True)
    state = fields.Selection([('open','Open'),('terminated','Terminated')],string='State',default='open')



    @api.one
    def button_open(self):
        self.state='open'

    @api.one
    def button_terminate(self):
        self.state='terminated'




    @api.onchange('vehicle_id')
    def onchange_vehicle(self):

        if(self.vehicle_id):
            today_str = fields.Date.today();
            today_date = datetime.strptime(today_str,DEFAULT_SERVER_DATE_FORMAT)
            today_month = today_date.month
            year_start_date = datetime(today_date.year,1,1,0,0)
            year_start_str = year_start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)

            #getting travel order number
            self.env.cr.execute("""SELECT t.num
                                   FROM fleet_vehicle_travel_order t
                                   WHERE t.vehicle_id="""+str(self.vehicle_id.id)+""" AND RIGHT(t.num,2)='"""+str(today_month)+"""' AND t.date>='"""+year_start_str+"""'
                                   ORDER BY t.num DESC
                                """)
            result = self.env.cr.fetchone() or ()

            if result:
                old_num = result[0]
                old_ordinal = old_num.split("/")[0]
                new_ordinal = int(old_ordinal) +1
                new_num = str(new_ordinal).zfill(2) + "/" + str(today_month)

            else:
                new_num = '01/' + str(today_month)

            self.num = new_num

            #getting travel order series
            self.env.cr.execute("SELECT MAX(CAST(t.series as INTEGER)) FROM fleet_vehicle_travel_order t WHERE  t.date>='"+year_start_str+"'")

            result = self.env.cr.fetchone() or ()
            if result and result[0]:
                old_series = result[0]
                new_series = old_series + 1
            else:
                new_series = 1

            self.series = str(new_series).zfill(6)



    @api.multi
    def return_fuel_logs(self):

        return  {
                    "type": "ir.actions.act_window",
                    "res_model": "fleet.vehicle.log.fuel",
                    "views": [[False, "tree"], [False, "form"]],
                    "domain": [["travel_order_id", "=", self[0].id]],
                    "context": {'default_travel_order_id':self[0].id,'default_vehicle_id':self[0].vehicle_id.id}
                }


    @api.v7
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            for this_obj_line in this_obj.travel_order_line_ids:
                self.pool.get('fleet.vehicle.travel.order.line').unlink(cr,1,this_obj_line.id)
        return super(fleet_vehicle_travel_order,self).unlink(cr,uid,ids,context=context)




