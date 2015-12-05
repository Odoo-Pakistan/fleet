# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Fleet Extension (v8)',
    'version': '0.00001',
    'author': 'B++',
    'category': 'Fleet Management System',
    'sequence': 01,
    'website': 'https://www.bplus.plus',
    'summary': 'Vehicles,Travel Orders',
    'description': """
Fleet Management System (v8)
==========================




    """,
    'author': 'B++',
    'website': 'https://www.bplus.plus',
    'depends': ['base','hr','v7_fleet_extend_universal'],
    'data': [
         'data/order_menuitems.xml',
         # 'data/remove_service_types.xml',
         # 'views/other_costs_view.xml',
         # 'views/travel_order_view.xml',
         'views/fleet_vehicle.xml',
         # 'views/services_view.xml',
         # 'views/contract_view.xml',
         # 'views/cost_view.xml',
         'views/cargo_values_view.xml',
         'security/ir.model.access.csv',

   ],

    'installable': True,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
