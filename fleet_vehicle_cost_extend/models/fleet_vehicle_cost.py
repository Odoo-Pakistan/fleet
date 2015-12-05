# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class FleetVehicleCost(models.Model):
    _inherit = 'fleet.vehicle.cost'

    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id, context=context).date
        if not date:
            date = fields.date.context_today(self, cr, uid, context=context)
        this_obj = self.browse(cr, uid, id, context=context)
        if this_obj.odometer_id:
            self.pool.get('fleet.vehicle.odometer').unlink(cr, 1, this_obj.odometer_id.id)
        vehicle_id = this_obj.vehicle_id
        data = {'value': value, 'date': date, 'vehicle_id': vehicle_id.id}
        odometer_id = self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        return self.write(cr, uid, id, {'odometer_id': odometer_id}, context=context)

    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr, uid, ids, context=context):
            if record.odometer_id:
                res[record.id] = record.odometer_id.value
        return res

    department_id = fields.Many2one('hr.department', string='Department')
    notes = fields.Text('Additional info')

    # TODO: Ovdje treba napraviti nekakav nacin za obavjestavanje i racunanje ovih vrijednosti
    alert = fields.Boolean('Alert')
    next_service = fields.Float('Next Service', default=0.0)
    next_service_in = fields.Float('Next Service In', default=0.0)

    # @api.onchange('alert')
    # def on_change_subtype(self):
    #     self.next_service = 0.0
    #     if self.alert and self.cost_subtype_id:
    #         self.next_service = self.cost_subtype_id.next_service
    #         self.next_service_in = self.next_service + self.parent_id.odometer_id.value

    # @api.onchange('next_service')
    # def on_change_next_service(self):
    #     self.next_service_in = 0.0
    #     if self.alert and self.parent_id.odometer_id and self.next_service:
    #         self.next_service_in = self.next_service + self.parent_id.odometer_id.value
