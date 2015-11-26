# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from dateutil.relativedelta import relativedelta
from openerp.osv.orm import except_orm
from openerp.tools.translate import _

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

def get_month_name(month):
        if (month == 1):
            return 'January'
        elif (month == 2):
            return 'February'
        elif (month == 3):
            return 'March'
        elif (month == 4):
            return 'April'
        elif (month == 5):
            return 'May'
        elif (month == 6):
            return 'June'
        elif (month == 7):
            return 'July'
        elif (month == 8):
            return 'August'
        elif (month == 9):
            return 'September'
        elif (month == 10):
            return 'October'
        elif (month == 11):
            return 'November'
        elif (month == 12):
            return 'December'
        else:
            return ''

class fleet_vehicle_tyre(osv.Model):
    
    _name = 'fleet.vehicle.tyre'
    _description = 'Tires on vehicles'
    
    _columns = {
            'name': fields.char('Position', size=128, required=True),
            'type': fields.selection([('winter','Winter tires'),('summer','Summer tires')], 'Type of tires'),
            'note': fields.text('Additional description'),
    }

class fleet_vehicle_gear(osv.Model):
    _name = 'fleet.vehicle.gear'
    _description = 'Additional gear in vehicle'
    
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'note': fields.text('Additional description'),
        'months':fields.integer('Months until alert')
    }


class fleet_vehicle_gear_rel(osv.Model):
    _name = 'fleet.vehicle.gear.rel'
    
    
    def _compute_alerts(self, cr, uid, ids, field_names, unknow_none, context=None):
        res= {}
        for record in self.browse(cr, uid, ids, context=context):
            overdue = False
            due_soon = False
            if record.alert:
                months_until = self.pool['fleet.vehicle.gear'].browse(cr,uid,record.gear_id.id,context).months
                current_date_str = fields.date.context_today(self, cr, uid, context=context)
                date_str = record.date
                current_date = str_to_datetime(current_date_str)
                date = str_to_datetime(date_str)
                date = date + relativedelta(months=months_until)
                diff_time = (date-current_date).days
                if diff_time < 0:
                    overdue = True
                if diff_time < 30 and diff_time >= 0:
                    due_soon = True;
    
    
    
            res[record.id] = {
            'overdue': overdue,
            'due_soon': due_soon,
            }
        return res
    
    _columns = {
           'gear_id' : fields.many2one('fleet.vehicle.gear',string='Gear',required=True),
           'vehicle_id': fields.many2one('fleet.vehicle',string='Vehicle'),
           'date' : fields.date('Date'),
           'alert':fields.boolean('Alert'),
           'due_soon':fields.function(_compute_alerts,type='boolean',multi='alerts'),
           'overdue':fields.function(_compute_alerts,type='boolean',multi='alerts')              
           
           }
    
    

class fleet_vechile_type(osv.Model):
    
    _name = 'fleet.vehicle.type'
    _description = 'Fleet vehicle type'
    
    
    _columns = {
            'name': fields.char('Name', size=128, required=True),
            'reg_required': fields.boolean('Registration required?'),
            'measure': fields.selection([('km','Kilometers'),('hour','Working hours')],'Measure unit'),
            'vehicle_ids': fields.one2many('fleet.vehicle', 'type_id', 'Vehicles'),
    }

class fleet_vechile(osv.Model):
    
    _inherit = 'fleet.vehicle'
    
    _name = 'fleet.vehicle'
    
    
    def _get_default_amortization_type(self, cr, uid, context):
        try:
            model, model_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fleet_extend', 'type_service_amortization')
        except ValueError:
            model_id = False
        return model_id
    
    def _get_default_type(self, cr, uid, context):
        try:
            model, type_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fleet_extend', 'fleet_vehicle_type_5')
        except ValueError:
            type_id = False
        return type_id
    
    def _get_transport_capacity(self, cr, uid, ids, field_names, args, context={}):
        res = {}
        
        for id in ids:
            vh_mass = self.browse(cr, uid, id).mass or 0
            vh_ent_mass = self.browse(cr, uid, id).entire_mass or 0
            if (vh_ent_mass - vh_mass < 0):
                res[id] = 0
            else:
                res[id] = vh_ent_mass - vh_mass 
        return res
    
    
    def _get_avg_fuel_consumption(self, cr, uid, ids, field_names, args, context={}):
        res = {}
        
        for id in ids:
            cr.execute(""" SELECT MIN(od.value) as min, MAX(od.value) as max, SUM(fuel.liter) as lit 
                            FROM fleet_vehicle_log_fuel fuel
                            JOIN fleet_vehicle_cost cost ON (fuel.cost_id = cost.id)
                            JOIN fleet_vehicle_odometer od ON (cost.odometer_id = od.id)
                            WHERE cost.vehicle_id = """ + str(id))
            result = cr.fetchone() or ()
            cr.execute(""" SELECT last.lit 
                            FROM (SELECT fuel.liter as lit 
                                    FROM fleet_vehicle_log_fuel fuel
                                    JOIN fleet_vehicle_cost cost ON (fuel.cost_id = cost.id)
                                    WHERE cost.vehicle_id = """ + str(id) + """
                                    ORDER BY fuel.id DESC
                                    LIMIT 1) last """)
            last_fuel = cr.fetchone() or ()
            if len(last_fuel)>0 and len(result)>0 and result[2]!=None and result[0]!=None and result[0]!=result[1]:
                liter = result[2] - last_fuel[0]
                odo_max = result[1]
                odo_min = result[0]
                if odo_max-odo_min!=0:
                    avg = (liter/(odo_max-odo_min))*100
                else:
                    avg = 0
                res[id] = avg
            else:
                res[id] = 0
         
        return res
    
    def _search_get_overdue_contract_reminder(self, cr, uid, obj, name, args, context):
        res = []
        for field, operator, value in args:
            assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'
            today = fields.date.context_today(self, cr, uid, context=context)
            cr.execute('select cost.vehicle_id, count(contract.id) as contract_number FROM fleet_vehicle_cost cost left join fleet_vehicle_log_contract contract on contract.cost_id = cost.id WHERE contract.expiration_date is not null AND contract.expiration_date < %s AND contract.state IN (\'open\', \'toclose\') GROUP BY cost.vehicle_id', (today,))
            res_ids = [x[0] for x in cr.fetchall()]
            res.append(('id', search_operator, res_ids))
        return res
    
    def _search_contract_renewal_due_soon(self, cr, uid, obj, name, args, context):
        res = []
        for field, operator, value in args:
            assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'
            today = fields.date.context_today(self, cr, uid, context=context)
            datetime_today = datetime.datetime.strptime(today, tools.DEFAULT_SERVER_DATE_FORMAT)
            limit_date = str((datetime_today + relativedelta(days=+30)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT))
            cr.execute('select cost.vehicle_id, count(contract.id) as contract_number FROM fleet_vehicle_cost cost left join fleet_vehicle_log_contract contract on contract.cost_id = cost.id WHERE contract.expiration_date is not null AND contract.expiration_date > %s AND contract.expiration_date < %s AND contract.state IN (\'open\', \'toclose\') GROUP BY cost.vehicle_id', (today, limit_date))
            res_ids = [x[0] for x in cr.fetchall()]
            res.append(('id', search_operator, res_ids))
        return res
         
    def _get_contract_reminder_fnc(self, cr, uid, ids, field_names, unknow_none, context=None):
        res= {}
        for record in self.browse(cr, uid, ids, context=context):
            overdue = False
            due_soon = False
            total = 0
            name = ''
            for element in record.log_contracts:
                if element.state in ('open', 'toclose') and element.expiration_date:
                    current_date_str = fields.date.context_today(self, cr, uid, context=context)
                    due_time_str = element.expiration_date
                    current_date = str_to_datetime(current_date_str)
                    due_time = str_to_datetime(due_time_str)
                    diff_time = (due_time-current_date).days
                    if diff_time < 0:
                        overdue = True
                        total += 1
                    if diff_time < 30 and diff_time >= 0:
                            due_soon = True;
                            total += 1
                    if overdue or due_soon:
                        ids = self.pool.get('fleet.vehicle.log.contract').search(cr,uid,[('vehicle_id', '=', record.id), ('state', 'in', ('open', 'toclose'))], limit=1, order='expiration_date asc')
                        if len(ids) > 0:
                            #we display only the name of the oldest overdue/due soon contract
                            name=(self.pool.get('fleet.vehicle.log.contract').browse(cr, uid, ids[0], context=context).cost_subtype_id.name)

            res[record.id] = {
                'contract_renewal_overdue': overdue,
                'contract_renewal_due_soon': due_soon,
                'contract_renewal_total': (total - 1), #we remove 1 from the real total for display purposes
                'contract_renewal_name': name,
            }
        return res
    
    

        
    def _count_travel_orders(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            TravelOrder = self.pool['fleet.vehicle.travel.order']
            res[id] = TravelOrder.search_count(cr, uid, [('vehicle_id', '=', id)], context=context)
        return res      
     
    _columns = {
            'type_id': fields.many2one('fleet.vehicle.type', 'Vehicle type'),
            'reg_required': fields.boolean('Registration required?'),
            'avg_fuel_consumption': fields.function(_get_avg_fuel_consumption, type="float", string='Average fuel consumption'),
            'gps_num': fields.char('GPS number', size=64),
            'year_manufactured': fields.char('Year of manufacturing'),
            'country_id': fields.many2one('res.country', string='Country'),
            'engine_volume_ccm3': fields.integer('Engine volume in ccm3'),
            'engine_num': fields.char('Engine number', size=64),
            'mass': fields.integer('Vehicle mass'),
            'entire_mass': fields.integer('Entire mass'),
            'transport_capacity': fields.function(_get_transport_capacity, type="integer", string="Transport mass capacity", readonly=True),
            'tyre_ids': fields.many2many('fleet.vehicle.tyre','fleet_vehicle_tyre_rel', 'vehicle_id', 'tyre_id', string='Tires'),
            'gear_ids': fields.one2many( 'fleet.vehicle.gear.rel','vehicle_id', string='Gear'),
            'department_id': fields.many2one('hr.department', string='Company department'),
            'contract_renewal_due_soon': fields.function(_get_contract_reminder_fnc, fnct_search=_search_contract_renewal_due_soon, type="boolean", string='Has Contracts to renew', multi='contract_info'),
            'contract_renewal_overdue': fields.function(_get_contract_reminder_fnc, fnct_search=_search_get_overdue_contract_reminder, type="boolean", string='Has Contracts Overdued', multi='contract_info'),
            'contract_renewal_name': fields.function(_get_contract_reminder_fnc, type="text", string='Name of contract to renew soon', multi='contract_info'),
            'contract_renewal_total': fields.function(_get_contract_reminder_fnc, type="integer", string='Total of contracts due or overdue minus one', multi='contract_info'),
            'notes': fields.text('Additional information'),
            'technical_inspection_date': fields.date('Technical inspection date'),
            '6_months_technical_inspection': fields.boolean('Every 6 months'),
            'amortization_ids': fields.one2many('fleet.vehicle.amortization', 'vehicle_id', string='Amortization'),
            'amortization_factor': fields.float('Amortization factor', digits=(12,2)),
            'salvage_value': fields.float('Salvage value', digits=(12,2)),
            'travel_order_ids': fields.one2many('fleet.vehicle.travel.order', 'vehicle_id', 'Travel Orders'),
            'travel_order_count': fields.function(_count_travel_orders, type='integer', string='Travel Orders'),
    }
    
    _defaults = {
        'type_id': _get_default_type,
        'technical_inspection_date': False,
        'amortization_factor': 0.2,
        'salvage_value': 2000.0,
    }
    
    
    
    def generate_amortization(self, cr, uid, ids, context={}):
        am_obj = self.pool.get('fleet.vehicle.amortization')
        cost_obj = self.pool.get('fleet.vehicle.cost')
        veh_objs = self.browse(cr, uid, ids)
        amort_type = self._get_default_amortization_type(cr, uid, context)
        for veh_obj in veh_objs:
            
            calculation_ok = veh_obj.acquisition_date and veh_obj.car_value
            if not calculation_ok:
                continue
            
            cost_ids = am_obj.search(cr, uid, [('vehicle_id','=',veh_obj.id)])
            am_obj.unlink(cr, uid, cost_ids)
            cost_ids = cost_obj.search(cr, uid, [('vehicle_id','=',veh_obj.id),('cost_type','=','other'),('cost_subtype_id','=',amort_type)])
            cost_obj.unlink(cr, uid, cost_ids)
                        
            month = time.strptime(veh_obj.acquisition_date, tools.DEFAULT_SERVER_DATE_FORMAT).tm_mon
            year = time.strptime(veh_obj.acquisition_date, tools.DEFAULT_SERVER_DATE_FORMAT).tm_year
            
            date = str_to_datetime(str(year) + '-' + str(month) + '-01')
            vpurchase = veh_obj.car_value
            vmoment = vpurchase
            factor = veh_obj.amortization_factor
            vsalvage = veh_obj.salvage_value
            amount = (vpurchase * factor) / 12
            vals = {}
            
            if (factor<0 and factor>=1):
                continue
            if (vsalvage<0 and vsalvage>=vpurchase):
                continue
            
            
            while(True):
                
                if (vmoment-vsalvage <= amount):
                    amount = vmoment-vsalvage
                    vmoment = vsalvage
                    vals = {
                        'vehicle_id': veh_obj.id,
                        'date': date.strftime('%Y-%m-%d'),
                        'cost_type': 'other',
                        'cost_subtype_id': amort_type,
                        'amount': amount,
                        'parent_id': False,
                    }
                    am_obj.create(cr, uid, vals)
                    vals = {}
                    break
                
                vals = {
                    'vehicle_id': veh_obj.id,
                    'date': date.strftime('%Y-%m-%d'),
                    'cost_type': 'other',
                    'cost_subtype_id': amort_type,
                    'amount': amount,
                    'parent_id': False,
                }
                am_obj.create(cr, uid, vals)
                vals = {}
                date = date + relativedelta(months=1)
                vmoment -= amount    
        
        return False
    
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'fleet', context['xml_id'], context=context)
            if context.get('search_default_group_dep'):
                del context['search_default_group_dep']
            if context.get('group_by'):
                del context['group_by']
            res['context'] = context
            res['context'].update({'default_vehicle_id': ids[0]})
            res['domain'] = [('vehicle_id','=', ids[0])]
            return res
        return False
    
    def return_action_to_open_travel_orders(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}
      
        if context.get('xml_id'):
            if 'group_by' in context:
                del context['group_by']
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'v7_fleet_extend_universal', context['xml_id'], context=context)
            res['context'] = context
            res['domain'] = [('vehicle_id','=', ids[0])]
            res['context'].update({'default_vehicle_id': ids[0]})
            return res
        return False
    
    def onchange_type(self, cr, user, ids, type_id, context={}):
        model = self.pool.get('fleet.vehicle.type')
        obj = model.read(cr, user, type_id, ['reg_required'])
        if obj:
            reg_required = obj.get('reg_required', False)
            return {
                'value': {'reg_required': reg_required}
                }
        else:
            return True
        
        
        
        
        
        
        
        
        
class fleet_vehicle_travel_order(osv.Model):
         
    _name='fleet.vehicle.travel.order'
    _rec_name='num'
    



    def onchange_vehicle(self,cr,user,ids,vehicle_id,context={}):
           
        today = fields.date.context_today(self, cr, user, context=context)
        month=str(today).split('-',5)[1]
        year=str(today).split('-',5)[0]
        year=year+'-01'+'-01'
        vehicle_id = vehicle_id or 0
        cr.execute("""SELECT t.num
                      FROM fleet_vehicle_travel_order t
                      WHERE t.vehicle_id="""+str(vehicle_id)+""" AND RIGHT(t.num,2)='"""+month+"""' AND t.date>='"""+year+"""'
                      ORDER BY t.num DESC                          
                                  
        """)
          
        rez=cr.fetchone() or ()
        string = ''
        if rez:
            string=rez[0]
            string=str(int(rez[0].split('/',5)[0])+1)+'/'+str(rez[0].split('/',5)[1])
            if string!='' and (int(string.split('/')[0]) < 10):
                string='0'+string

        else:
            string='01/'+month
        

        cr.execute("SELECT MAX(t.series) FROM fleet_vehicle_travel_order t WHERE  t.date>='"+year+"'")
        rez2=cr.fetchone() or ()   
        
        
        
        if rez2:
            series=rez2[0]
            
            if series:
                series=int(series)+1
            else:
                series=1
                
            if(series<10):
                series='00000'+str(series)
            elif(series<100):
                series='0000'+str(series)
            elif(series<1000):
                series='000'+str(series)
            elif(series<10000):
                series='00'+str(series)
            elif(series<100000):
                series='0'+str(series)
            else:
                series=str(series)
        else:
            series='000001'
        
        rez = {                   
               'value':{
                        'num':string,
                        'series':series,
                        }
                }         
        
        return rez
     
    def _check_odometer_validity(self,cr,uid,id,value,check_type,context):
    #provjerava da li je start veci od stop vrijednosti i suprotno
    #ako je check_type = start onda je pozvana iz start odometra
        this_obj = self.browse(cr, uid, id, context=context)
        if(check_type == 'start'):
            if not this_obj.stop_odometer_id:
                return True
            odometer_value = this_obj.stop_odometer_id.value
            if value > odometer_value:
                return False
            else:
                return True
        else:
            if not this_obj.start_odometer_id:
                return True
            odometer_value = this_obj.start_odometer_id.value
            if value < odometer_value:
                return False
            else:
                return True
            
        
        
        
     
    def _set_start_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
        if(self._check_odometer_validity(cr, uid, id, value,'start', context) == False):
            raise except_orm(_('Odometer error'),_('Start odometer value must not be bigger than stop odometer value'))
        
        this_obj =self.browse(cr, uid, id, context=context)
        #ako postoji neki zapis vezan za ovo polje, ukloni ga 
        if(this_obj.start_odometer_id):
            self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.start_odometer_id.id)
            
        vehicle_id = this_obj.vehicle_id.id 
        data = {'value': value, 'vehicle_id': vehicle_id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'start_odometer_id': odometer_id}, context=context)

    def _set_stop_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
        if(self._check_odometer_validity(cr, uid, id, value,'stop', context) == False):
            raise except_orm(_('Odometer error'),_('Stop odometer value must not be lower than start odometer value'))
        
        this_obj =self.browse(cr, uid, id, context=context)
        #ako postoji neki zapis vezan za ovo polje, ukloni ga 
        if(this_obj.stop_odometer_id):
            self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.stop_odometer_id.id)
        
        vehicle_id = this_obj.vehicle_id.id
        data = {'value': value, 'vehicle_id': vehicle_id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'stop_odometer_id': odometer_id}, context=context)
     
    def _get_start_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.start_odometer_id:
                res[record.id] = record.start_odometer_id.value
            else:
                res[record.id] = 0
                
        return res
    
    def _get_stop_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.stop_odometer_id:
                res[record.id] = record.stop_odometer_id.value
            else:
                res[record.id] = 0
        return res
    
    def _get_fuel_log_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = len(self.browse(cr,uid,id,context).fuel_log_ids)
        return res 
             
     
    _columns={
               'vehicle_id':fields.many2one('fleet.vehicle','Vehicle',required=True),
               'additional_vehicle_id':fields.many2one('fleet.vehicle','Additional Vehicle'),
               'place': fields.char('Place',size=64),
               'date':fields.date('Date', required=True),
               'num':fields.char("Number",size=64,required=True),
               'type' : fields.selection([('cargo','PN3'),('passenger','PN4')],'Type'),
               'driver1_id':fields.many2one('hr.employee','1st Driver',required=False),
               'driver2_id':fields.many2one('hr.employee','2nd Driver'),
               'codriver1_id':fields.many2one('hr.employee','1st Co-Driver'),
               'codriver2_id':fields.many2one('hr.employee','2nd Co-Driver'),
               'codriver3_id':fields.many2one('hr.employee','3rd Co-Driver'),
               'codriver4_id':fields.many2one('hr.employee','4th Co-Driver'),
               'cargo_worker1_id':fields.many2one('hr.employee','1st Cargo Worker'),  
               'cargo_worker2_id':fields.many2one('hr.employee','2nd Cargo Worker'),
               'cargo_worker3_id':fields.many2one('hr.employee','3rd Cargo Worker'),
               'cargo_worker4_id':fields.many2one('hr.employee','4th Cargo Worker'),            
               'distance':fields.char('Distance',size=256,required=True),  
               'fuel_log_ids':fields.one2many('fleet.vehicle.log.fuel','travel_order_id'),
               'fuel_log_count':fields.function(_get_fuel_log_count,type="integer",string='Fuel Logs'),
               'travel_order_line_ids':fields.one2many('fleet.vehicle.travel.order.line','travel_order_id'),  
               'series':fields.char('Series', size=64, required=False),
               'start_odometer_id': fields.many2one('fleet.vehicle.odometer', 'Odometer start', help='Odometer measure of the vehicle at the moment of this log'),
               'start_odometer': fields.function(_get_start_odometer, fnct_inv=_set_start_odometer, type='float', string='Odometer start', help='Odometer measure of the vehicle at the moment of this log'),
               'stop_odometer_id': fields.many2one('fleet.vehicle.odometer', 'Odometer stop', help='Odometer measure of the vehicle at the moment of this log'),
               'stop_odometer': fields.function(_get_stop_odometer, fnct_inv=_set_stop_odometer, type='float', string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log'),            
        }
    
    _defaults = {
            'place': 'Draksenić',
            'date' : fields.datetime.now(),            
        }
    
    
    
    def return_action_to_open_view(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'fleet', context['xml_id'], context=context)
            context['default_travel_order_id']=ids[0]
            res['context'] = context
            res['domain'] = [('travel_order_id','=', ids[0])]
            return res
        return False
        
    def create(self, cr, uid, data, context=None):
        #ako nisu setovani da se ne bi pozivala funckija za setovanje
        if 'start_odometer' in data and not data['start_odometer']:
           del(data['start_odometer'])
        if 'stop_odometer' in data and not data['stop_odometer']:
           del(data['stop_odometer'])
        return super(fleet_vehicle_travel_order, self).create(cr, uid, data, context=context)
    
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if (this_obj.start_odometer_id):
                self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.start_odometer_id.id)
            if (this_obj.stop_odometer_id):
                self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.stop_odometer_id.id)
        return super(fleet_vehicle_travel_order,self).unlink(cr,uid,ids,context=context)
        

class fleet_vehicle_travel_order_line(osv.Model):
    
    _name = 'fleet.vehicle.travel.order.line'
         
    def _set_odometer(self, cr, user, travel_order_id, value, context=None):
         
        date = fields.date.context_today(self, cr, user, context=context)  
        tmp=self.pool.get('fleet.vehicle.travel.order').browse(cr, user, travel_order_id, context=context)  
        #tmp=self.browse(cr,user,id,context=context)    
         
    #    vehicle_id = self.pool.get('fleet.vehicle.travel.order').browse(cr,user,tmp.travel_order_id,context=context).vehicle_id
        data = {'value': value, 'date': date, 'vehicle_id': tmp.vehicle_id.id}
        self.pool.get('fleet.vehicle.odometer').create(cr, user, data, context=context)
        return
    
    
    
    def _set_start_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id).date
        vehicle_id = self.browse(cr, uid, id, context=context).travel_order_id.vehicle_id.id
        data = {'value': value, 'date': date, 'vehicle_id': vehicle_id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'start_odometer_id': odometer_id}, context=context)

    def _set_stop_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id).date
        vehicle_id = self.browse(cr, uid, id, context=context).travel_order_id.vehicle_id.id
        data = {'value': value, 'date': date, 'vehicle_id': vehicle_id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'stop_odometer_id': odometer_id}, context=context)
     
    def _get_start_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.start_odometer_id:
                res[record.id] = record.start_odometer_id.value
            else:
                res[record.id] = 0
        return res
    
    def _get_stop_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.stop_odometer_id:
                res[record.id] = record.stop_odometer_id.value
            else:
                res[record.id] = 0
        return res
          
    _columns={
              'date':fields.date('Datum'),
              'distance':fields.char('Distance',size=64),
              'travel_order_id':fields.many2one('fleet.vehicle.travel.order'),
              'start_odometer_id': fields.many2one('fleet.vehicle.odometer', 'Odometer start', help='Odometer measure of the vehicle at the moment of this log'),
              'start_odometer': fields.function(_get_start_odometer, fnct_inv=_set_start_odometer, type='float', string='Odometer start', help='Odometer measure of the vehicle at the moment of this log'),
              'stop_odometer_id': fields.many2one('fleet.vehicle.odometer', 'Odometer stop', help='Odometer measure of the vehicle at the moment of this log'),
              'stop_odometer': fields.function(_get_stop_odometer, fnct_inv=_set_stop_odometer, type='float', string='Odometer stop', help='Odometer measure of the vehicle at the moment of this log'),                             
        }
    
class fleet_vehicle_cost(osv.Model):
    _name = 'fleet.vehicle.cost'
    _inherit = 'fleet.vehicle.cost'
    
    
    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'),_('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id, context=context).date
        if not(date):
            date = fields.date.context_today(self, cr, uid, context=context)
    
        this_obj = self.browse(cr, uid, id, context=context)
        if(this_obj.odometer_id):
            self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.odometer_id.id)
        
        vehicle_id = this_obj.vehicle_id
        data = {'value': value, 'date': date, 'vehicle_id': vehicle_id.id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'odometer_id': odometer_id}, context=context)
    
    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.odometer_id:
                res[record.id] = record.odometer_id.value
        return res
    
    
       
    _columns = {
            'department_id': fields.related('vehicle_id', 'department_id', store=True, relation='hr.department', type='many2one', string='Department'),
            'odometer': fields.function(_get_odometer, fnct_inv=_set_odometer, type='float', string='Odometer Value', help='Odometer measure of the vehicle at the moment of this log'),
        }  
    
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if (this_obj.odometer_id):
                self.pool.get('fleet.vehicle.odometer').unlink(cr,1,this_obj.odometer_id.id)
        return super(fleet_vehicle_cost,self).unlink(cr,uid,ids,context=context)
               
         
        
class fleet_vehicle_log_fuel(osv.Model):
    _name='fleet.vehicle.log.fuel'
    _inherit='fleet.vehicle.log.fuel'
    
    _columns={
              'travel_order_id':fields.many2one('fleet.vehicle.travel.order','Travel Order'),
              'department_id': fields.related('vehicle_id', 'department_id',store=True, relation='hr.department', type='many2one', string='Department'),
        }
    
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if(this_obj.cost_id):
                self.pool.get('fleet.vehicle.cost').unlink(cr,1,this_obj.cost_id.id)
        return super(fleet_vehicle_log_fuel,self).unlink(cr,uid,ids,context=context)

class fleet_vehicle_log_services(osv.Model):
    _name = 'fleet.vehicle.log.services'
    _inherit = 'fleet.vehicle.log.services'

    _columns = {
            'department_id': fields.related('vehicle_id', 'department_id', store=True, relation='hr.department', type='many2one', string='Department'),
        }
        
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if(this_obj.cost_id):
                self.pool.get('fleet.vehicle.cost').unlink(cr,1,this_obj.cost_id.id)
        return super(fleet_vehicle_log_services,self).unlink(cr,uid,ids,context=context)
        
        
class fleet_vehicle_log_contract(osv.Model):
    
    _name = 'fleet.vehicle.log.contract'
    _inherit = 'fleet.vehicle.log.contract'
    
    
    _columns = {
            'is_deposited': fields.boolean('Is contract deposited?'),
            'department_id': fields.related('vehicle_id', 'department_id',store=True, relation='hr.department', type='many2one', string='Department'),
    }  
    
    def unlink(self,cr,uid,ids,context=None):
        this_objs = self.browse(cr,uid,ids,context=context)
        for this_obj in this_objs:
            if(this_obj.cost_id):
                self.pool.get('fleet.vehicle.cost').unlink(cr,1,this_obj.cost_id.id)
        return super(fleet_vehicle_log_contract,self).unlink(cr,uid,ids,context=context)   


class fleet_vehicle_amortization(osv.Model):
    

    
    _inherits = {'fleet.vehicle.cost': 'cost_id'}
    _name = 'fleet.vehicle.amortization'
    _description = 'Amortization for vehicles'
    
    
    
    def _get_default_service_type(self, cr, uid, context):
        try:
            model, model_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fleet_extend', 'type_service_amortization')
        except ValueError:
            model_id = False
        return model_id
    
    def _month_get_fnc(self, cr, uid, ids, name, unknow_none, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            if (record.date):
                res[record.id] = str(time.strptime(record.date, tools.DEFAULT_SERVER_DATE_FORMAT).tm_year) + ' ' + get_month_name(time.strptime(record.date, tools.DEFAULT_SERVER_DATE_FORMAT).tm_mon)
            else:
                res[record.id] = _('Unknown')
        return res

#     Kad se pravi amortizacija treba samo unijeti pocetni datum za mjesec i automatski
#     ce se popuniti polje month

    _columns = {
        'cost_id': fields.many2one('fleet.vehicle.cost', 'Cost', required=True, ondelete='cascade'),
        'cost_amount': fields.related('cost_id', 'amount', string='Amount', type='float', store=True), #we need to keep this field as a related with store=True because the graph view doesn't support (1) to address fields from inherited table and (2) fields that aren't stored in database
        'month': fields.function(_month_get_fnc, type='char', string='Month', store=True),
        'notes': fields.text('Notes'),
    }
    
    
    
    _defaults = {
        'cost_subtype_id': _get_default_service_type,
        'cost_type': 'other',
    }
