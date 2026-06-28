# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import pandas as pd
from odoo import api, fields, models
from odoo.exceptions import UserError


class FleetMaintenanceImport(models.TransientModel):
    _name = "fleet.maintenance.import"
    _description = "Import Maintenance Records from Excel"

    file = fields.Binary(string="Excel File", required=True)
    filename = fields.Char(string="Filename")

    def import_maintenance_records(self):
        """Import maintenance records from Excel file"""
        try:
            # Read the Excel file with all sheets
            xl = pd.ExcelFile(self.file, engine='openpyxl')

            # Map sheet names to maintenance categories
            sheet_category_map = {
                'الزيت': 'oil',
                'البنزين': 'fuel',
                'الكاوتش': 'tires',
                'تيل الفرامل': 'brakes',
                'البوجيهات': 'spark_plugs',
                'الكاتينة': 'timing_belt',
                'الطنابير': 'hoses',
                'الدبرياج': 'clutch',
                'البطارية': 'battery',
                'الصيانة العامة': 'general',
                'خط السير': 'route',
                'مصروفات متنوعة ': 'misc',
                'بيانات حادث': 'accident',
                '44533': 'vehicle',
            }

            # Get the current user and company
            user = self.env.user
            company = user.company_id

            total_imported = 0

            # Process each sheet
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet_name, engine='openpyxl')
                category = sheet_category_map.get(sheet_name, 'general')

                # Process each row in the sheet
                for index, row in df.iterrows():
                    # Skip empty rows
                    if pd.isna(row.get('التاريخ', None)):
                        continue

                    # Create a new maintenance record
                    self.env['fleet.vehicle.maintenance'].create({
                        'name': f"{category.upper()}-{index+1}",
                        'vehicle_id': self._get_vehicle(row.get('السيارة', '')),
                        'date': row['التاريخ'] if not pd.isna(row['التاريخ']) else fields.Date.today(),
                        'maintenance_category': category,
                        'description': row.get('بيـــــــــــــــــان', ''),
                        'quantity': row.get('عدد', 1),
                        'unit_price': row.get('السعر', 0),
                        'parts_cost': row.get('القيمة', 0),
                        'odometer': row.get('عداد الصيانة', 0),
                        'previous_odometer': row.get('المعدل', 0),
                        'vendor_id': self._get_service_provider(row.get('المصنعية', '')),
                        'technician_id': self._get_driver(row.get('القائم بالعمل', '')),
                        'driver_id': self._get_driver(row.get('السائق', '')),
                        'company_id': company.id,
                        'notes': row.get('ملاحظات', ''),
                    })

                    total_imported += 1

            # Return a success message
            return {
                'type': 'ir.actions.act_window_close',
                'message': f'Successfully imported {total_imported} maintenance records from {len(xl.sheet_names)} sheets.',
            }

        except Exception as e:
            raise UserError(f"Error importing maintenance records: {str(e)}")

    def _get_vehicle(self, vehicle_name):
        """Get or create a vehicle by name"""
        if not vehicle_name:
            return False

        vehicle = self.env['fleet.vehicle'].search([('license_plate', '=', vehicle_name)], limit=1)
        if not vehicle:
            # Create a new vehicle if it doesn't exist
            vehicle = self.env['fleet.vehicle'].create({
                'license_plate': vehicle_name,
                'company_id': self.env.user.company_id.id,
            })

        return vehicle.id

    def _get_service_provider(self, provider_name):
        """Get or create a service provider by name"""
        if not provider_name:
            return False

        provider = self.env['res.partner'].search([('name', '=', provider_name)], limit=1)
        if not provider:
            # Create a new service provider if it doesn't exist
            provider = self.env['res.partner'].create({
                'name': provider_name,
                'is_company': True,
                'company_type': 'company',
                'customer': True,
                'supplier': True,
            })

        return provider.id

    def _get_driver(self, driver_name):
        """Get or create a driver by name"""
        if not driver_name:
            return False

        driver = self.env['res.partner'].search([('name', '=', driver_name)], limit=1)
        if not driver:
            # Create a new driver if it doesn't exist
            driver = self.env['res.partner'].create({
                'name': driver_name,
                'is_company': False,
                'company_type': 'person',
            })

        return driver.id
