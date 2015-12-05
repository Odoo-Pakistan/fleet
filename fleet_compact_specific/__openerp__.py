# -*- encoding: utf-8 -*-

{
    "name" : "Fleet management - Compact doo",
    "description" : """
Module for specific things in Fleet management system
===========================================================
Module for specific things in Fleet management system
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicles and contracts",

    'depends': [
        'fleet',
        'hr',
        'fleet_extend',
        'fleet_vehicle_cost_extend',
        'fleet_travel_order',
        'fleet_travel_order_costs',
        'fleet_order_menu_items',
    ],
    'data':[
        'wizard/generate_xls_reports_view.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: