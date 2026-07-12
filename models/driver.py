from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotDriver(models.Model):
    _name = 'fleetpilot.driver'
    _description = 'FleetPilot Driver'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Driver Name', required=True, tracking=True)
    license_number = fields.Char(string='License Number', required=True, tracking=True)
    license_expiry = fields.Date(string='License Expiry Date', required=True, tracking=True)
    
    phone = fields.Char(string='Phone Number', tracking=True)
    email = fields.Char(string='Email Address', tracking=True)
    
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('suspended', 'Suspended'),
        ('on_leave', 'On Leave'),
    ], string='Status', default='available', tracking=True, required=True)
    
    active = fields.Boolean(default=True)
    
    # Relationships
    vehicle_ids = fields.One2many('fleetpilot.vehicle', 'driver_id', string='Assigned Vehicles')
    trip_ids = fields.One2many('fleetpilot.trip', 'driver_id', string='Trips')

    _sql_constraints = [
        ('license_number_uniq', 'unique(license_number)', 'The driver license number must be unique!'),
    ]

    @api.constrains('license_expiry')
    def _check_license_expiry(self):
        for rec in self:
            if rec.license_expiry and rec.license_expiry < fields.Date.context_today(rec):
                raise ValidationError(_('The driver license has expired or expiry date is in the past!'))
