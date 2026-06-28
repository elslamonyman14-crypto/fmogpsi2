# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class FleetVehicleMaintenance(models.Model):
    _name = "fleet.vehicle.maintenance"
    _description = "Vehicle Maintenance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    # === Basic Information ===
    name = fields.Char(string="Reference", required=True, copy=False, default="New")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", required=True, tracking=True)
    date = fields.Date(string="Maintenance Date", required=True, default=fields.Date.context_today, tracking=True)
    
    # === Maintenance Category (14 Excel sheets) ===
    maintenance_category = fields.Selection(
        [
            ("oil", "Oil (الزيت)"),
            ("fuel", "Fuel (البنزين)"),
            ("tires", "Tires (الكاوتش)"),
            ("brakes", "Brakes (تيل الفرامل)"),
            ("spark_plugs", "Spark Plugs (البوجيهات)"),
            ("timing_belt", "Timing Belt (الكاتينة)"),
            ("hoses", "Hoses (الطنابير)"),
            ("clutch", "Clutch (الدبرياج)"),
            ("battery", "Battery (البطارية)"),
            ("general", "General Maintenance (الصيانة العامة)"),
            ("route", "Route/Trip (خط السير)"),
            ("misc", "Misc Expenses (مصروفات متنوعة)"),
            ("accident", "Accident Data (بيانات حادث)"),
            ("vehicle", "Vehicle Info (44533)"),
        ],
        string="Maintenance Category",
        tracking=True,
    )
    
    service_type_id = fields.Many2one("fleet.service.type", string="Service Type", tracking=True)
    service_category = fields.Selection(
        [
            ("repair", "Repair"),
            ("inspection", "Inspection"),
            ("routine", "Routine"),
            ("upgrade", "Upgrade"),
        ],
        string="Service Category",
        default="repair",
        tracking=True,
    )
    
    # === Cost Information ===
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity", default=1.0)
    unit_price = fields.Monetary(string="Unit Price")
    parts_cost = fields.Monetary(string="Parts Cost", compute="_compute_parts_cost", store=True)
    labor_cost = fields.Monetary(string="Labor Cost", default=0.0)
    other_cost = fields.Monetary(string="Other Cost", default=0.0)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", store=True)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", readonly=True)
    
    # === Odometer Information ===
    odometer = fields.Float(string="Odometer", tracking=True)
    previous_odometer = fields.Float(string="Previous Odometer")
    duration_hours = fields.Float(string="Duration (hours)")
    
    # === Service Provider ===
    vendor_id = fields.Many2one("res.partner", string="Vendor", tracking=True)
    technician_id = fields.Many2one("res.partner", string="Technician", tracking=True)
    driver_id = fields.Many2one("res.partner", string="Driver")
    
    # === Warranty ===
    warranty_number = fields.Char(string="Warranty Reference")
    warranty_end_date = fields.Date(string="Warranty End Date", tracking=True)
    warranty_remaining_days = fields.Integer(string="Warranty Remaining Days", compute="_compute_warranty_remaining_days", store=True)
    
    # === Planning ===
    planned_date = fields.Date(string="Planned Date", tracking=True)
    next_service_date = fields.Date(string="Next Service Date", tracking=True)
    service_location = fields.Char(string="Service Location", tracking=True)
    
    # === Other ===
    priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
        string="Priority",
        default="medium",
        tracking=True,
    )
    notes = fields.Text(string="Notes")
    
    # === State ===
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)

    # === CRUD & Workflow ===
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("fleet.vehicle.maintenance") or "New"
        return super().create(vals_list)

    def action_schedule(self):
        self.filtered(lambda r: r.state == "draft").write({"state": "scheduled"})

    def action_done(self):
        self.filtered(lambda r: r.state in ("draft", "scheduled")).write({"state": "done"})

    def action_cancel(self):
        self.filtered(lambda r: r.state != "cancelled").write({"state": "cancelled"})

    # === Compute Methods ===
    @api.depends("quantity", "unit_price")
    def _compute_parts_cost(self):
        for r in self:
            r.parts_cost = (r.quantity or 0.0) * (r.unit_price or 0.0)

    @api.depends("parts_cost", "labor_cost", "other_cost")
    def _compute_total_cost(self):
        for r in self:
            r.total_cost = (r.parts_cost or 0.0) + (r.labor_cost or 0.0) + (r.other_cost or 0.0)

    @api.depends("warranty_end_date", "date")
    def _compute_warranty_remaining_days(self):
        for r in self:
            if r.warranty_end_date and r.date:
                r.warranty_remaining_days = (
                    fields.Date.from_string(r.warranty_end_date)
                    - fields.Date.from_string(r.date)
                ).days
            else:
                r.warranty_remaining_days = 0

    @api.constrains("odometer")
    def _check_odometer(self):
        for r in self:
            if r.odometer < 0:
                raise UserError("Odometer value cannot be negative.")
