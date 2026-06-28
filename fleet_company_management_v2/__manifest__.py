# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Fleet Company Management",
    "summary": "Manage company cars, fuel logs, maintenance and rates for fleet vehicles with Excel import support.",
    "version": "18.0.1.0.0",
    "category": "Human Resources/Fleet",
    "author": "Company",
    "website": "https://github.com/yourusername/fleet_company_management",
    "license": "AGPL-3",
    "depends": ["fleet"],
    "data": [
        "security/fleet_company_management_security.xml",
        "security/ir.model.access.csv",
        "data/fleet_company_management_data.xml",
        "views/fleet_menu.xml",
        "views/fleet_vehicle_maintenance_views.xml",
        "views/fleet_vehicle_fuel_views.xml",
        "views/fleet_vehicle_rate_views.xml",
        "views/fleet_maintenance_import_views.xml",
        "views/gps_tracking_menu.xml",
    ],
    "external_dependencies": {"python": ["psycopg2", "pandas", "openpyxl"]},
    "installable": True,
    "application": True,
}
