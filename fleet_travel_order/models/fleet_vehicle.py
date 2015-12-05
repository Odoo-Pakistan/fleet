# -*- coding: utf-8 -*-

from openerp import models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

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