# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicleLogOtherCost(models.Model):

    _name = 'fleet.vehicle.log.other.cost'
    _description = 'Other costs for vehicles'
    _inherits = {'fleet.vehicle.cost': 'cost_id'}

    name = fields.Char('Name')
    cost_id = fields.Many2one('fleet.vehicle.cost', string='Cost', required=True, ondelete='cascade')
    purchaser_id = fields.Many2one('res.partner', string='Purchaser', domain="[('employee','=',True)]")
    vendor_id = fields.Many2one('res.partner', string='Supplier', domain="[('supplier','=',True)]")
    inv_ref = fields.Char(string='Invoice Reference')
#     cost_amount = fields.Float (related='cost_id.amount',string='Amount',store=True)

    @api.multi
    def unlink(self):
        for obj in self:
            if (obj.cost_id):
                obj.cost_id.unlink()
        return super(FleetVehicleLogOtherCost, self).unlink()


# u modelu cost je vec po defaultu cost_type = other

#napraviti oncahnge za vehicle_id...koja popunjava odometer