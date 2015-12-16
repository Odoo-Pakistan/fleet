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

                obj.contract_renewal_due_soon = due_soon
                obj.contract_renewal_overdue  = overdue



    @api.multi
    def _search_contract_renewal_due_soon(self):
        pass

    @api.multi
    def _search_get_overdue_contract_reminder(self):
        pass

    contract_renewal_due_soon = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_contract_renewal_due_soon,string='Has Contracts to renew')
    contract_renewal_overdue  = fields.Boolean(compute=_get_contract_reminder_fnc, search=_search_get_overdue_contract_reminder,string='Has Contracts Overdued')

    @api.multi
    def _get_services_reminder_fnc(self):
        pass
    def _search_services_due_soon(self):
        pass
    def _search_services_overdue(self):
        pass

    @api.multi
    def _get_services_info(self):
        pass

    @api.one
    def show_alerted_services(self):
        return self.env.ref('fleet_alerts.fleet_vehicle_alert_cost_action')
        #     {
        #     "type": "ir.actions.act_window",
        #     "res_model": "fleet.vehicle.cost",
        #     "views": [[False, "tree"], [False, "form"]],
        #     "view_id": self.env.ref("fleet_alerts.fleet_vehicle_cost_tree_simple"),
        #     "domain": [["vehicle_id", "=", self[0].id], ["alert", "=", True]], #OVDJE DODATI DA JE I OVERDUE I DUE SOON = TRUE
        #     "context": {}
        # }

    services_due_soon = fields.Boolean(compute=_get_services_reminder_fnc, search=_search_services_due_soon, string='Has Services to do soon')
    services_overdue = fields.Boolean(compute=_get_services_reminder_fnc, search=_search_services_overdue, string='Has Services overdue')
    services_info = fields.Html(compute=_get_services_info, string='Services Info')
