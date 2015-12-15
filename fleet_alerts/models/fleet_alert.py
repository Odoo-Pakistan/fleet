from openerp import fields,models



class FleetAlert(models.Model):
    
    _name='fleet.alert'
    
    name = fields.Char('Name')
    is_alert_set = fields.Boolean("Is alert set")
    due_soon_days = fields.Float("Days for due soon expiration alert?",default=0)
#     for_all = fields.Boolean("For all")
#     only_for = fields.Boolean("Only for")
#     not_for = fields.Boolean("Not for")
    