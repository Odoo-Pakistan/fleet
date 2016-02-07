import time

from openerp.report import report_sxw

class fleet_travel_order_parser(report_sxw.rml_parse):
    
    
    def _empty_rows(self, niz):
        if(len(niz)>10):
            return [None]
        return [ None for i in range(10-len(niz)) ] 
    
    def __init__(self, cr, uid, name, context=None):
        super(fleet_travel_order_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'empty_rows':self._empty_rows,
        })
    

class fleet_travel_order_parser_passenger(report_sxw.rml_parse):    
    
        def _empty_rows(self, niz):
            if(len(niz)>10):
                return [None]
            return [ None for i in range(10-len(niz)) ] 
        
    
    
        def __init__(self, cr, uid, name, context=None):
            super(fleet_travel_order_parser_passenger, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                                      'time': time, 
                                      'empty_rows':self._empty_rows,
        })
     

    

report_sxw.report_sxw('report.fleet.travel.order.report.passenger', 'fleet.vehicle.travel.order',
                      'addons/v7_fleet_extend_universal/report/fleet_travel_order_passenger.rml',
                       parser=fleet_travel_order_parser, header=False)


report_sxw.report_sxw('report.fleet.travel.order.report.cargo', 'fleet.vehicle.travel.order',
                      'addons/v7_fleet_extend_universal/report/fleet_travel_order_cargo.rml',
                       parser=fleet_travel_order_parser_passenger, header=False)