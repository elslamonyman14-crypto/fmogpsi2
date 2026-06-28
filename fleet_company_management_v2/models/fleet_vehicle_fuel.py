# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class FleetVehicleFuel(models.Model):
    _name = "fleet.vehicle.fuel"
    _description = "Vehicle Fuel Log"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    name = fields.Char(string="Reference", required=True, copy=False, default="New")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", required=True, tracking=True)
    date = fields.Date(string="Fuel Date", required=True, default=fields.Date.context_today, tracking=True)
    
    # === Fuel Information ===
    fuel_type = fields.Selection(
        [
            ("gasoline", "Gasoline"),
            ("diesel", "Diesel"),
            ("electric", "Electric"),
            ("hybrid", "Hybrid"),
            ("lpg", "LPG"),
        ],
        string="Fuel Type",
        required=True,
        default="gasoline",
        tracking=True,
    )
    
    # === Quantity and Cost ===
    liters = fields.Float(string="Liters", required=True, tracking=True)
    price_per_liter = fields.Monetary(string="Price per Liter", tracking=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", store=True)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", readonly=True)
    
    # === Odometer ===
    odometer = fields.Float(string="Odometer", required=True, tracking=True)
    previous_odometer = fields.Float(string="Previous Odometer")
    distance_traveled = fields.Float(string="Distance Traveled (km)", compute="_compute_distance_traveled", store=True)
    
    # === Efficiency ===
    consumption_per_100km = fields.Float(string="Consumption (L/100km)", compute="_compute_consumption", store=True)
    
    # === Location ===
    location = fields.Char(string="Fuel Station Location")
    vendor_id = fields.Many2one("res.partner", string="Fuel Station", tracking=True)
    
    # === Additional ===
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("fleet.vehicle.fuel") or "New"
        return super().create(vals_list)

    @api.depends("liters", "price_per_liter")
    def _compute_total_cost(self):
        for r in self:
            r.total_cost = (r.liters or 0.0) * (r.price_per_liter or 0.0)

    @api.depends("odometer", "previous_odometer")
    def _compute_distance_traveled(self):
        for r in self:
            r.distance_traveled = r.odometer - (r.previous_odometer or 0.0)

    @api.depends("liters", "distance_traveled")
    def _compute_consumption(self):
        for r in self:
            if r.distance_traveled > 0:
                r.consumption_per_100km = (r.liters / r.distance_traveled) * 100
            else:
                r.consumption_per_100km = 0.0

    @api.constrains("odometer")
    def _check_odometer(self):
        for r in self:
            if r.odometer < 0:
                raise UserError("Odometer value cannot be negative.")
