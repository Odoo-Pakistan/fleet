# -*- encoding: utf-8 -*-

{
    "name" : "Fleet - Service and cost features extension",
    "description" : """
Extension of service and cost features
==========================
Module for extending service and cost features of Fleet management module
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicles and contracts",

    'depends': [
        'fleet',
        'hr',
    ],
    'data':[
        'data/remove_service_types.xml',
        'views/vehicle_service_type_view.xml',
        'views/vehicle_log_services_view.xml',
        'views/vehicle_log_fuel_view.xml',
        'views/vehicle_log_contract_view.xml',
        'views/vehicle_log_other_cost_view.xml',
        'views/vehicle_cost_view.xml',
        'views/menuitems.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: