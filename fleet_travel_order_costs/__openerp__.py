# -*- encoding: utf-8 -*-

{
    "name" : "Fleet - Travel order and vehicle costs relationship",
    "description" : """
Travel order + vehicle costs
=========================================================================
This module makes relationship between travel orders and vehicle costs
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicles and contracts",

    'depends': [
        'fleet_vehicle_cost_extend',
        'fleet_travel_order',
    ],
    'data':[
        'views/vehicle_log_fuel_view.xml',
        'views/vehicle_cost_view.xml',
        'views/vehicle_travel_order_view.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: