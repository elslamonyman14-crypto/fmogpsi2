# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FleetVehicleRate(models.Model):
    _name = "fleet.vehicle.rate"
    _description = "Vehicle Rate"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_from desc"

    name = fields.Char(string="Reference", required=True, copy=False, default="New")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", required=True, tracking=True)
    
    # === Rate Period ===
    date_from = fields.Date(string="Valid From", required=True, default=fields.Date.context_today, tracking=True)
    date_to = fields.Date(string="Valid To", tracking=True)
    
    # === Rates ===
    rate_per_km = fields.Monetary(string="Rate per km", tracking=True)
    rate_per_hour = fields.Monetary(string="Rate per hour", tracking=True)
    daily_rate = fields.Monetary(string="Daily Rate", tracking=True)
    fixed_rate = fields.Monetary(string="Fixed Rate", tracking=True)
    
    # === Additional Costs ===
    fuel_included = fields.Boolean(string="Fuel Included", default=False)
    driver_included = fields.Boolean(string="Driver Included", default=False)
    
    notes = fields.Text(string="Notes")
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("fleet.vehicle.rate") or "New"
        return super().create(vals_list)
