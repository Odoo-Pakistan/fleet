# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetInvoice(models.Model):
    _name = 'fleet.invoice'
    _rec_name = 'broj_fakture'

    travel_order_id = fields.Many2one('fleet.vehicle.travel.order', 'Putni nalog')

    broj_fakture = fields.Char('Broj fakture', required=True)
    osnovica = fields.Float('Osnovica')
    pdv = fields.Float('PDV')
    ukupan_iznos = fields.Float('Ukupan iznos', required=True)

    prevezeno_tona = fields.Float('Prevezeno tona')
    cijena_po_toni_EUR = fields.Float('Cijena po toni €')
    cijena_po_toni_KM = fields.Float('Cijena po toni KM')
