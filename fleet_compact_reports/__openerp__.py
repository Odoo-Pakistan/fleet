# -*- encoding: utf-8 -*-

{
    "name" : "Fleet reports - Compact doo",
    "description" : """
Fleet management system reports
==========================
Module for advanced reports of Fleet management system
""",
    "version" : "1.00",
    "author" : "B++",
    "category" : "Managing vehicles and contracts",

    'depends': [
        'fleet',
        'hr',
    ],
    'data':[
        'wizard/generate_xls_reports_view.xml',
    ],

    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: