# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    @api.depends('cost_ids.amount')
    def _get_tmp_amount(self):
        for rec in self:
            amm = 0
            if rec.cost_ids:
                for line in rec.cost_ids:
                    amm += line.amount
                if rec.amount != amm:
                    self.write({'amount': amm})
                rec.tmp_amount = amm

    @api.multi
    def _has_alerts(self):
        for rec in self:
            odometer = rec.odometer
            vehicle_odometer = rec.vehicle_id.odometer
            for line in rec.cost_ids:
                if line.alert:
                    diff = (odometer+line.next_service) - vehicle_odometer
                    if diff < 10000.0:
                        rec.has_alerts = True

    def _search_alerts(self, operator, value):
        assert operator in ('=', '!=', '<>') and value in (True, False), _('Operation not supported')
        res_ids=[]
        if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
            search_operator = 'in'
        else:
            search_operator = 'not in'
        for rec in self.search([]):
            if rec.has_alerts:
                res_ids.append(rec.id)
        return [('id', search_operator, res_ids)]

    tmp_amount = fields.Float('TMP_AMM', compute=_get_tmp_amount)
    has_alerts = fields.Boolean('Has Alerts', compute=_has_alerts, search=_search_alerts)

    @api.multi
    def unlink(self):
        for obj in self:
            for child_cost in obj.cost_ids:
                child_cost.sudo().unlink()
            if obj.cost_id:
                obj.cost_id.sudo().unlink()
        return super(FleetVehicleLogServices, self).unlink()

