# -*- encoding: utf-8 -*-

{
    "name" : "Fleet Extension",
    "description" : """
Added new fields
==========================
Module for extending core fleet with new field and functionalities
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicles and contracts",

    'depends': [
        'fleet',
    ],
    'data':[
        'data/vehicle_type_data.xml',
        'views/fleet_vehicle_view.xml',
        'views/res_config_view.xml',
        'data/order_menuitems.xml',
        'security/ir.model.access.csv',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
