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
        'views/fleet_vehicle_view.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
