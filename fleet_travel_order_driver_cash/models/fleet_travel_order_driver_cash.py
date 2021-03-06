from openerp import models,fields,api


class FleetTravelOrderDriverCash(models.Model):

    _name = "fleet.travel.order.driver.cash"

    @api.one
    def _get_name(self):
        self.name = self.travel_order_id.series + '/' + (self.currency_id.name or '')

    @api.multi
    def _compute_returned_amount(self):
        self.returned_amount = 0

    @api.multi
    @api.depends('received_amount', 'returned_amount')
    def _compute_diff_amount(self):
        for rec in self:
            rec.diff_amount = (rec.received_amount or 0) - (rec.returned_amount or 0)

    name = fields.Char(compute=_get_name, string='Name')
    travel_order_id = fields.Many2one('fleet.vehicle.travel.order')
    currency_id = fields.Many2one('res.currency', string='Currency')
    received_amount = fields.Float('Received amount')
    returned_amount = fields.Float(string='Returned amount')
    diff_amount = fields.Float(compute=_compute_diff_amount, string='Spent amount')
    currency_rate = fields.Float(string="Currency rate")
#     cost_ids = fields.One2many('fleet.vehicle.cost', 'driver_cash_id', 'Costs paid')






