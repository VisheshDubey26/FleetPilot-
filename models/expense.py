
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FleetpilotExpense(models.Model):
    _name = 'fleetpilot.expense'
    _description = 'FleetPilot Expense Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Expense Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    vehicle_id = fields.Many2one('fleetpilot.vehicle', string='Vehicle', required=True, tracking=True)
    driver_id = fields.Many2one('fleetpilot.driver', string='Driver', tracking=True)
    
    date = fields.Date(string='Expense Date', default=fields.Date.context_today, required=True, tracking=True)
    
    expense_type = fields.Selection([
        ('toll', 'Toll Charges'),
        ('fine', 'Fine / Penalty'),
        ('insurance', 'Insurance premium'),
        ('tax', 'Road Tax'),
        ('repair', 'Repairs & Spare parts'),
        ('other', 'Other Expenses'),
    ], string='Expense Type', default='toll', required=True, tracking=True)
    
    amount = fields.Float(string='Amount', required=True, tracking=True)
    invoice_ref = fields.Char(string='Invoice / Receipt Reference', tracking=True)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', default='draft', tracking=True, required=True)
    
    description = fields.Text(string='Description / Justification')

    @api.model_create_multi
    def create(self, vals_list):
        for v in vals_list:
            if v.get('name', _('New')) == _('New'):
                v['name'] = self.env['ir.sequence'].next_by_code('fleetpilot.expense') or _('New')
        return super(FleetpilotExpense, self).create(vals_list)

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0.0:
                raise ValidationError(_('Expense amount must be greater than zero!'))

    def action_submit(self):
        self.ensure_one()
        self.write({'status': 'submitted'})

    def action_approve(self):
        self.ensure_one()
        self.write({'status': 'approved'})

    def action_refuse(self):
        self.ensure_one()
        self.write({'status': 'refused'})
