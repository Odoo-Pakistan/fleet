# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FleetVehicleTravelOrder(models.Model):
    _inherit = 'fleet.vehicle.travel.order'


    @api.multi
    @api.depends('invoice_ids.ukupan_iznos')
    def _compute_ukupan_iznos_ture(self):
        for obj in self:
            ukupno = 0
            for invoice in self.invoice_ids:
                if invoice.ukupan_iznos:
                    ukupno += invoice.ukupan_iznos
            self.ukupan_iznos_ture = ukupno


    invoice_ids = fields.One2many('fleet.invoice', 'travel_order_id', string='Fakture')
    ukupan_iznos_ture = fields.Float(string='Ukupan iznos ture',compute=_compute_ukupan_iznos_ture,store=True)