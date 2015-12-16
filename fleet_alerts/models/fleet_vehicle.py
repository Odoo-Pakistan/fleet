from openerp import models,fields,api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
                total = 0
                overdue = False
                due_soon = False
                name = ''

                for obj_contract in obj.log_contracts:
                    if obj_contract.state in ('open','toclose') and obj_contract.expiration_date:
                        today_date_str = fields.Date.today()
                        expiration_date_str = obj_contract.expiration_date
                        today_date = datetime.strptime(today_date_str,DEFAULT_SERVER_DATE_FORMAT)
                        expiration_date = datetime.strptime(expiration_date_str,DEFAULT_SERVER_DATE_FORMAT)
                        diff_time = (expiration_date - today_date).days
                        if diff_time < 0:
                            overdue = True
                            total += 1
                        if diff_time < overdue_days and diff_time >=0:
                            due_soon=True
                            total += 1
                if due_soon or overdue:
                    name = self.env['fleet.vehicle.log.contract'].search([('vehicle_id', '=', obj.id), ('state', 'in', ('open', 'toclose'))], limit=1, order='expiration_date asc')[0].cost_subtype_id.name

                obj.contract_renewal_due_soon = due_soon
                obj.contract_renewal_overdue  = overdue
                obj.contract_renewal_total = total
                obj.contract_renewal_name = name



    @api.multi
    def _search_contract_renewal_due_soon(self,operator,value):
        assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
        alert_rules = self.env.ref('fleet_alerts.contract_renewal_alert')
        alert_active = False
        if alert_rules:
            alert_active = alert_rules.is_alert_set
        if alert_active:
            due_soon_days = alert_rules.due_soon_days
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'

            today_str = fields.Date.today()
            today_date = datetime.strptime(today_str, DEFAULT_SERVER_DATE_FORMAT)
            limit_date = str((today_date + relativedelta(days=+due_soon_days)).strftime(DEFAULT_SERVER_DATE_FORMAT))
            self.env.cr.execute("""select cost.vehicle_id, count(contract.id) as contract_number
                                   FROM fleet_vehicle_cost cost left join fleet_vehicle_log_contract contract on contract.cost_id = cost.id
                                   WHERE contract.expiration_date is not null AND contract.expiration_date > %s AND contract.expiration_date < %s AND contract.state IN (\'open\', \'toclose\')
                                   GROUP BY cost.vehicle_id""", (today_str, limit_date))
            res_ids = [x[0] for x in self.env.cr.fetchall()]

        return [('id', search_operator, res_ids)]

    @api.multi
    def _search_get_overdue_contract_reminder(self,operator,value):
        assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
        alert_rules = self.env.ref('fleet_alerts.contract_renewal_alert')
        alert_active = False
        if alert_rules:
            alert_active = alert_rules.is_alert_set
        if alert_active:
            due_soon_days = alert_rules.due_soon_days
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'
            today_str = fields.Date.today()
            self.env.cr.execute("""select cost.vehicle_id, count(contract.id) as contract_number
                                   FROM fleet_vehicle_cost cost left join fleet_vehicle_log_contract contract on contract.cost_id = cost.id
                                   WHERE contract.expiration_date is not null AND contract.expiration_date < %s AND contract.state IN (\'open\', \'toclose\')
                                   GROUP BY cost.vehicle_id""", (today_str,))
            res_ids = [x[0] for x in self.env.cr.fetchall()]

        return [('id', search_operator, res_ids)]

    contract_renewal_due_soon = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_contract_renewal_due_soon,string='Has Contracts to renew')
    contract_renewal_overdue = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_get_overdue_contract_reminder,string='Has Contracts Overdued')
    contract_renewal_name = fields.Char(compute=_get_contract_reminder_fnc,string='Name of contract to renew soon')
    contract_renewal_total = fields.Float(compute=_get_contract_reminder_fnc,string='Total of contracts due or overdue minus one')
