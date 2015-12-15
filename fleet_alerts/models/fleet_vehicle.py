from openerp import models,fields,api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


class FleetVehicle(models.Model):
    
    _name='fleet.vehicle'
    _inherit = 'fleet.vehicle'
    
    
    @api.multi
    def _get_contract_reminder_fnc(self):      
        
        alert_rules = self.env.ref('fleet_alerts.contract_renewal_alert')
        alert_active = False
        if alert_rules:
            alert_active = alert_rules.is_alert_set
         
        if alert_active:
            overdue_days = alert_rules.due_soon_days
            
            for obj in self:
                overdue = False;
                due_soon = False;
    
                
                for obj_contract in obj.log_contracts:
                    if obj_contract.state in ('open','toclose') and obj_contract.expiration_date:
                        today_date_str = fields.Date.today();
                        expiration_date_str = obj_contract.expiration_date
                        today_date = datetime.strptime(today_date_str,DEFAULT_SERVER_DATE_FORMAT)
                        expiration_date = datetime.strptime(expiration_date_str,DEFAULT_SERVER_DATE_FORMAT)
                        diff_time = (expiration_date - today_date).days
                        if diff_time < 0:
                            overdue = True
                        if diff_time < overdue_days and diff_time >=0:
                            due_soon=True
                 
                obj.contract_due_soon = due_soon
                obj.contract_overdue  = overdue

     
     
    @api.multi
    def _search_contract_renewal_due_soon(self):
        pass
 
    @api.multi
    def _search_get_overdue_contract_reminder(self):
        pass
     
    contract_due_soon = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_contract_renewal_due_soon,string='Has Contracts to renew')
    contract_overdue  = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_get_overdue_contract_reminder, type="boolean", string='Has Contracts Overdued')


