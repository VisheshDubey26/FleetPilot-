
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotFuelLog(models.Model):
    _name = 'fleetpilot.fuel.log'
    _description = 'FleetPilot Fuel Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    vehicle_id = fields.Many2one('fleetpilot.vehicle', string='Vehicle', required=True, tracking=True)
    driver_id = fields.Many2one('fleetpilot.driver', string='Driver', tracking=True)
    
    date = fields.Date(string='Refueling Date', default=fields.Date.context_today, required=True, tracking=True)
    liter = fields.Float(string='Liters Filled', required=True, tracking=True)
    price_per_liter = fields.Float(string='Price Per Liter', required=True, tracking=True)
    amount = fields.Float(string='Total Cost', compute='_compute_amount', store=True, tracking=True)
    
    odometer = fields.Float(string='Odometer (km)', tracking=True)
    inv_ref = fields.Char(string='Invoice Reference', tracking=True)
    notes = fields.Text(string='Notes')

    @api.depends('liter', 'price_per_liter')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.liter * rec.price_per_liter

    @api.constrains('liter')
    def _check_liter(self):
        for rec in self:
            if rec.liter <= 0.0:
                raise ValidationError(_('Liters filled must be greater than zero!'))

    @api.constrains('price_per_liter')
    def _check_price_per_liter(self):
        for rec in self:
            if rec.price_per_liter < 0.0:
                raise ValidationError(_('Price per liter cannot be negative!'))

    @api.constrains('odometer')
    def _check_odometer(self):
        for rec in self:
            if rec.odometer and rec.odometer < 0.0:
                raise ValidationError(_('Odometer value cannot be negative!'))
