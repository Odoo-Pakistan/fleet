# -*- coding: utf-8 -*-

from openerp import models, fields, api

class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    @api.multi
    @api.depends('alert', 'next_service_relative', 'parent_id.odometer_id')
    def _compute_next_service_absolute(self):
        for rec in self:
            rec.next_service_absolute = 0.0
            if rec.alert and rec.parent_id.odometer_id and rec.next_service_relative:
                rec.next_service_absolute = rec.next_service_relative + rec.parent_id.odometer_id.value


    @api.multi
    def _compute_alerts(self):
        for rec in self:
            overdue = False
            due_soon = False
            alert_rule = self.env.ref('fleet_alerts.services_alert')
            alert_active = False
            border = 0.0
            if alert_rule:
                alert_active = alert_rule.is_alert_set
                border = alert_rule.due_soon_days or 0.0
            if alert_active and rec.alert:
                odometer = rec.vehicle_id.odometer or 0.0
                diff = rec.next_service_absolute - odometer
                if (diff < border) and (diff > 0):
                    due_soon = True
                elif (diff < border) and (diff <= 0):
                    overdue = True
            rec.overdue = overdue
            rec.due_soon = due_soon

    @api.multi
    def _search_services_due_soon(self, operator, value):
        assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
        alert_rule = self.env.ref('fleet_alerts.services_alert')
        alert_active = False
        if alert_rule:
            alert_active = alert_rule.is_alert_set
        if alert_active:
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'
            res_ids = []
            for rec in self.env['fleet.vehicle.cost'].search([]):
                if rec.due_soon:
                    res_ids.append(rec.id)
        return [('id', search_operator, res_ids)]

    @api.multi
    def _search_services_overdue(self, operator, value):
        assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
        alert_rule = self.env.ref('fleet_alerts.services_alert')
        alert_active = False
        if alert_rule:
            alert_active = alert_rule.is_alert_set
        if alert_active:
            if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
                search_operator = 'in'
            else:
                search_operator = 'not in'
            res_ids = []
            for rec in self.env['fleet.vehicle.cost'].search([]):
                if rec.overdue:
                    res_ids.append(rec.id)
        return [('id', search_operator, res_ids)]

    @api.multi
    def _compute_parent_odometer(self):
        for rec in self:
            rec.parent_odometer = rec.parent_id.odometer or 0

#   TODO: Ovdje treba napraviti nekakav nacin za obavjestavanje i racunanje ovih vrijednosti
    alert = fields.Boolean('Alert')
    parent_odometer = fields.Float('Odometer', compute=_compute_parent_odometer)
    next_service_relative = fields.Float('Next Service', default=0.0)
    next_service_absolute = fields.Float(compute=_compute_next_service_absolute, string='Next Service Absolute', default=0.0)
    due_soon = fields.Boolean(string='Due Soon', compute=_compute_alerts, search=_search_services_due_soon)
    overdue = fields.Boolean(string='Overdue', compute=_compute_alerts, search=_search_services_overdue)

    @api.onchange('alert', 'cost_subtype_id', 'parent_id.odometer_id')
    def on_change_subtype(self):
        self.next_service_relative = 0.0
        if self.alert and self.cost_subtype_id.next_service:
            self.next_service_relative = self.cost_subtype_id.next_service
            self.next_service_absolute = self.cost_subtype_id.next_service + (self.parent_id.odometer_id.value or 0)

    @api.one
    def make_done(self):
        self.alert = False
