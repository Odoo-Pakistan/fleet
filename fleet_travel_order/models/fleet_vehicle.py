# -*- coding: utf-8 -*-

from openerp import models,fields,api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    @api.multi
    def _compute_travel_order_count(self):
        for obj in self:
            obj.travel_order_count = len(obj.travel_order_ids)

    travel_order_ids = fields.One2many('fleet.vehicle.travel.order', 'vehicle_id', 'Travel Orders')
    travel_order_count = fields.Integer(compute = _compute_travel_order_count, string='Travel Orders')
    
    @api.v7
    def return_action_to_open_travel_orders(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}

        if context.get('xml_id'):
            if "group_by" in context:
                del context['group_by']
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, "fleet_travel_order", context['xml_id'], context=context)
            res['context'] = context
            res['domain'] = [('vehicle_id', '=', ids[0])]
            res['context'].update({'default_vehicle_id': ids[0]})
            return res
        return False
    
    
    
    
    