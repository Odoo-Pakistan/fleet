# -*- encoding: utf-8 -*-

{
    "name" : "Fleet - Travel order driver cash",
    "description" : """
Driver cash
==========================
Managing driver budget per travel order
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicle travel orders",

    'depends': [
        'fleet',
        'hr',
        'fleet_travel_order',
        'fleet_travel_order_costs',
    ],
    'data':[
#         'views/travel_order_view.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
