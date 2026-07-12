# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotTrip(models.Model):
    _name = 'fleetpilot.trip'
    _description = 'FleetPilot Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Trip Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    vehicle_id = fields.Many2one('fleetpilot.vehicle', string='Vehicle', required=True, tracking=True)
    driver_id = fields.Many2one('fleetpilot.driver', string='Driver', required=True, tracking=True)
    
    start_date = fields.Datetime(string='Start Date', default=fields.Datetime.now, required=True, tracking=True)
    end_date = fields.Datetime(string='End Date', tracking=True)
    
    route_from = fields.Char(string='Route From', required=True, tracking=True)
    route_to = fields.Char(string='Route To', required=True, tracking=True)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('complete', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, required=True)
    
    distance_covered = fields.Float(string='Distance Covered (km)', tracking=True)
    notes = fields.Text(string='Special Notes/Instructions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('fleetpilot.trip') or _('New')
        return super(FleetpilotTrip, self).create(vals_list)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.start_date > rec.end_date:
                raise ValidationError(_('The trip start date cannot be later than its end date!'))

    @api.constrains('distance_covered')
    def _check_distance(self):
        for rec in self:
            if rec.distance_covered < 0.0:
                raise ValidationError(_('Trip distance covered cannot be negative!'))

    def action_start_trip(self):
        self.ensure_one()
        if self.vehicle_id.status != 'available':
            raise ValidationError(_('The selected vehicle is currently not available!'))
        if self.driver_id.status != 'available':
            raise ValidationError(_('The selected driver is currently not available!'))
        
        self.write({'status': 'progress'})
        self.vehicle_id.write({'status': 'in_trip'})
        self.driver_id.write({'status': 'on_trip'})

    def action_complete_trip(self):
        self.ensure_one()
        self.write({
            'status': 'complete',
            'end_date': fields.Datetime.now()
        })
        self.vehicle_id.write({
            'status': 'available',
            'odometer': self.vehicle_id.odometer + self.distance_covered
        })
        self.driver_id.write({'status': 'available'})

    def action_cancel_trip(self):
        self.ensure_one()
        self.write({'status': 'cancel'})
        if self.vehicle_id.status == 'in_trip':
            self.vehicle_id.write({'status': 'available'})
        if self.driver_id.status == 'on_trip':
            self.driver_id.write({'status': 'available'})