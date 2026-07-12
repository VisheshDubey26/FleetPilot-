# -*- coding: utf-8 -*-
/**
 * @license
 * SPDX-License-Identifier: LGPL-3
 */

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotVehicle(models.Model):
    _name = 'fleetpilot.vehicle'
    _description = 'FleetPilot Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Vehicle Name', required=True, tracking=True)
    license_plate = fields.Char(string='License Plate', required=True, tracking=True)
    vehicle_type = fields.Selection([
        ('heavy_truck', 'Heavy Truck'),
        ('delivery_van', 'Delivery Van'),
        ('car', 'Passenger Car'),
        ('motorcycle', 'Motorcycle'),
    ], string='Vehicle Type', required=True, default='delivery_van', tracking=True)
    
    driver_id = fields.Many2one('fleetpilot.driver', string='Current Driver', tracking=True)
    
    status = fields.Selection([
        ('available', 'Available'),
        ('in_trip', 'In Trip'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ], string='Status', default='available', tracking=True, required=True)
    
    fuel_level = fields.Float(string='Fuel Level (%)', default=100.0, tracking=True)
    odometer = fields.Float(string='Odometer (km)', default=0.0, tracking=True)
    
    acquisition_date = fields.Date(string='Acquisition Date', default=fields.Date.context_today)
    next_maintenance_date = fields.Date(string='Next Scheduled Maintenance', tracking=True)
    
    active = fields.Boolean(default=True)
    
    # Relationships
    trip_ids = fields.One2many('fleetpilot.trip', 'vehicle_id', string='Trips')
    maintenance_ids = fields.One2many('fleetpilot.maintenance', 'vehicle_id', string='Maintenance Logs')
    fuel_log_ids = fields.One2many('fleetpilot.fuel.log', 'vehicle_id', string='Fuel Logs')
    expense_ids = fields.One2many('fleetpilot.expense', 'vehicle_id', string='Expenses')

    _sql_constraints = [
        ('license_plate_uniq', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

    @api.constrains('fuel_level')
    def _check_fuel_level(self):
        for rec in self:
            if rec.fuel_level < 0.0 or rec.fuel_level > 100.0:
                raise ValidationError(_('Fuel level must be between 0% and 100%!'))

    @api.constrains('odometer')
    def _check_odometer(self):
        for rec in self:
            if rec.odometer < 0.0:
                raise ValidationError(_('Odometer mileage cannot be negative!'))