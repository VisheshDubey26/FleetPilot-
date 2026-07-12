
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotMaintenance(models.Model):
    _name = 'fleetpilot.maintenance'
    _description = 'FleetPilot Maintenance Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'scheduled_date desc, id desc'

    name = fields.Char(string='Maintenance Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    title = fields.Char(string='Service Title', required=True, tracking=True)
    
    vehicle_id = fields.Many2one('fleetpilot.vehicle', string='Vehicle', required=True, tracking=True)
    
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Repair'),
        ('inspection', 'Routine Inspection'),
    ], string='Type', default='preventive', required=True, tracking=True)
    
    scheduled_date = fields.Date(string='Scheduled Date', default=fields.Date.context_today, required=True, tracking=True)
    completion_date = fields.Date(string='Completion Date', tracking=True)
    
    cost = fields.Float(string='Service Cost', default=0.0, tracking=True)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, required=True)
    
    description = fields.Text(string='Work Details / Diagnostics')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('fleetpilot.maintenance') or _('New')
        return super(FleetpilotMaintenance, self).create(vals_list)

    @api.constrains('cost')
    def _check_cost(self):
        for rec in self:
            if rec.cost < 0.0:
                raise ValidationError(_('Maintenance cost cannot be negative!'))

    @api.constrains('scheduled_date', 'completion_date')
    def _check_dates(self):
        for rec in self:
            if rec.scheduled_date and rec.completion_date and rec.scheduled_date > rec.completion_date:
                raise ValidationError(_('Completion date cannot be earlier than the scheduled date!'))

    def action_schedule(self):
        self.ensure_one()
        self.write({'status': 'scheduled'})

    def action_start_maintenance(self):
        self.ensure_one()
        self.write({'status': 'progress'})
        self.vehicle_id.write({'status': 'maintenance'})

    def action_complete_maintenance(self):
        self.ensure_one()
        self.write({
            'status': 'done',
            'completion_date': fields.Date.context_today(self)
        })
        self.vehicle_id.write({'status': 'available'})

    def action_cancel_maintenance(self):
        self.ensure_one()
        self.write({'status': 'cancel'})
        if self.vehicle_id.status == 'maintenance':
            self.vehicle_id.write({'status': 'available'})
