# -*- encoding: utf-8 -*-

{
    "name" : "Fleet Alerts",
    "description" : """
Managing fleet alerts
==========================
Managing alerts (Warning that vehicle contract has expired or will soon etc..)
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicle alerts",

    'depends': [
        'fleet_extend',
    ],
    'data':[
        'views/fleet_vehicle_view.xml',
        'views/fleet_alert_view.xml',
        'data/alerts.xml',
        
    ],

    "installable": True,
}
