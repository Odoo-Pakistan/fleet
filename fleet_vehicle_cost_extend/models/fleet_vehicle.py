# -*- coding: utf-8 -*-

from openerp import models,fields,api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    @api.multi
    def _compute_other_cost_count(self):
        for obj in self:
            obj.other_cost_count = len(obj.other_cost_ids)

    other_cost_ids = fields.One2many('fleet.vehicle.log.other.cost', 'vehicle_id', 'Other Costs')
    other_cost_count = fields.Integer(compute = _compute_other_cost_count, string='Other Costs')

    @api.v7
    def return_action_to_open_other_costs(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}

        if context.get('xml_id'):
            if "group_by" in context:
                del context['group_by']
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, "fleet_vehicle_cost_extend", context['xml_id'], context=context)
            res['context'] = context
            res['domain'] = [('vehicle_id', '=', ids[0])]
            res['context'].update({'default_vehicle_id': ids[0]})
            return res
        return False