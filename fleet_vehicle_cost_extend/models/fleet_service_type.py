# -*- coding: utf-8 -*-

from openerp import models, fields


class FleetServiceType(models.Model):
    _inherit = 'fleet.service.type'

    category = fields.Selection(
        [('contract', 'Contract'), ('service', 'Service'), ('both', 'Contract and Services'), ('fuel', 'Fuel'), ('other', 'Other')],
        string='Category', required=True, help='Choose wheter the service refer to contracts, vehicle services or both')
    parent_id = fields.Many2one('fleet.service.type', string='Parent')
    next_service = fields.Float('Next service', default=0.0)
