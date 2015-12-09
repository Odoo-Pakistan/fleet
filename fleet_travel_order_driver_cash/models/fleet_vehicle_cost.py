from openerp import fields,api,models




class FleetVehicleCost(models.Model):
    
    _inherit="fleet.vehicle.cost"
    _name="fleet.vehicle.cost"
    
    
    @api.one
    def _get_default_currency(self):
        pass
   
    #domain isti travel order da referenciraju
    driver_cash_id = fields.Many2one('fleet.travel.order.driver.cash',string='Payment method')
    #cak mozda da se currency popuni pomocu driver_cahs_id
    currency_id = fields.Many2one('res.currency',string='Currency',default= _get_default_currency)
    #provjera da li ima kesa
    #amount postoji
    amount = fields.Float('Amount')
    