# -*- coding: utf-8 -*-
/**
 * @license
 * SPDX-License-Identifier: LGPL-3
 */
{
    'name': 'FleetPilot',
    'version': '18.0.1.0.0',
    'summary': 'Advanced Fleet Management System for vehicles, drivers, trips, maintenance, and expenses.',
    'description': """
FleetPilot: Enterprise Fleet Operations & Logistics Suite
==========================================================
FleetPilot is a fully integrated fleet management module built for Odoo 18,
designed to optimize and coordinate vehicles, drivers, trips, maintenance scheduling,
fuel logging, and expense tracking.

Key Modules & Roles:
--------------------
* Vishesh (Team Leader): Core Module Setup, Manifest & Security, Menu Integration, Analytics Dashboard.
* Shashwat: Vehicle Lifecycle & Active Driver Profiling.
* Utkarsh: Trip Dispatch, Route Logistics & Live Workflows.
* Swayam: Maintenance Management, Fuel efficiency, and Expense optimization.

This module provides complete transparency of fleet operations and drives cost reduction
through preventive maintenance, route optimization, and live status dashboards.
    """,
    'category': 'Human Resources/Fleet',
    'author': 'Vishesh (Team Leader), Shashwat, Utkarsh, Swayam',
    'website': 'https://github.com/fleetpilot/fleetpilot',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/vehicle_views.xml',
        'views/driver_views.xml',
        'views/trip_views.xml',
        'views/maintenance_views.xml',
        'views/fuel_log_views.xml',
        'views/expense_views.xml',
        'views/dashboard_views.xml',
    ],
    'demo': [
        'data/fleetpilot_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
}