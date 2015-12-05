# -*- encoding: utf-8 -*-

{
    "name" : "Fleet - Travel orders",
    "description" : """
Travel orders
==========================
This module adds functionality for organizing travel orders, both for passenger and cargo vehicles
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicle travel orders",

    'depends': [
        'fleet',
        'hr',
    ],
    'data':[
        'views/travel_order_view.xml',
#              'views/travel_order_line_view.xml',
        'views/fleet_vehicle_log_fuel_view.xml',
#              'views/fleet_vehicle_type_view.xml',
#              'views/fleet_vehicle_tyre_view.xml',
#              'views/fleet_vehicle_gear_view.xml',
#              'views/fleet_vehicle_log_contract_view.xml',
#              'views/fleet_vehicle_view.xml',
#              'views/fleet_vehicle_cost_view.xml',
#              'views/fleet_vehicle_log_services_view.xml',
#              'views/travel_order_report_view.xml',
#              'data/vehicle_type_data.xml',
#              'data/vehicle_gear_data.xml',
#              'data/vehicle_cost_type_data.xml',
        'security/ir.model.access.csv',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: