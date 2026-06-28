# Fleet Company Management

An Odoo 18 module for managing company fleet vehicles, fuel logs, maintenance records, and vehicle rates with Excel import support.

## Features

- **Vehicle Maintenance**: Track maintenance records with 14 categories matching Excel sheet structure
  - Oil (الزيت), Fuel (البنزين), Tires (الكاوتش), Brakes (تيل الفرامل)
  - Spark Plugs (البوجيهات), Timing Belt (الكاتينة), Hoses (الطنابير)
  - Clutch (الدبرياج), Battery (البطارية), General Maintenance (الصيانة العامة)
  - Route/Trip (خط السير), Misc Expenses (مصروفات متنوعة), Accident Data (بيانات حادث)

- **Fuel Logs**: Track fuel consumption, costs, and efficiency calculations
- **Vehicle Rates**: Define rate structures per vehicle (per km, per hour, daily, fixed)
- **Excel Import**: Import maintenance data from multi-sheet Excel files with Arabic column names
- **Analytics**: Built-in graph and pivot views for maintenance and fuel analysis
- **Workflow**: Draft → Scheduled → Done states for maintenance records

## Installation

### Prerequisites

- Odoo 18
- Python 3.10+
- Docker (if using containerized deployment)

### Setup

1. **Install Python Dependencies**

   **Windows:**
   ```bash
   setup.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   pip install pandas openpyxl
   ```

2. **Copy Module to Odoo Addons**

   Copy the `fleet_company_management_v2` directory to your Odoo addons path:
   ```
   /path/to/odoo/addons/fleet_company_management_v2
   ```

3. **Update Module List**

   In Odoo:
   - Go to Apps → Update Apps List
   - Search for "Fleet Company Management"
   - Click Install

## Excel Import Format

The Excel file should contain the following sheets:

| Sheet Name (Arabic) | Category Key | Description |
|---------------------|--------------|-------------|
| الزيت | oil | Oil changes |
| البنزين | fuel | Fuel logs |
| الكاوتش | tires | Tire changes |
| تيل الفرامل | brakes | Brake service |
| البوجيهات | spark_plugs | Spark plugs |
| الكاتينة | timing_belt | Timing belt |
| الطنابير | hoses | Hoses |
| الدبرياج | clutch | Clutch service |
| البطارية | battery | Battery replacement |
| الصيانة العامة | general | General maintenance |
| خط السير | route | Route/trip data |
| مصروفات متنوعة | misc | Miscellaneous expenses |
| بيانات حادث | accident | Accident records |
| 44533 | vehicle | Vehicle information |

### Expected Columns per Sheet

- التاريخ (Date)
- عداد الصيانة (Odometer)
- المعدل (Previous Odometer)
- بيان (Description)
- عدد (Quantity)
- السعر (Unit Price)
- القيمة (Total Value)
- المصنعية (Service Provider)
- القائم بالعمل (Technician)
- السائق (Driver)
- ملاحظات (Notes)

## Usage

### Maintenance Records

1. Go to **Fleet Company → Maintenance**
2. Click **Create** to add a new maintenance record
3. Select the vehicle, date, and maintenance category
4. Fill in cost details and odometer readings
5. Save

### Import from Excel

1. Go to **Fleet Company → Import from Excel**
2. Upload your Excel file with the required sheets
3. Click **Import**
4. Records will be created automatically with appropriate categories

### Fuel Logs

1. Go to **Fleet Company → Fuel Logs**
2. Click **Create** to add a fuel log
3. Enter liters, price per liter, and odometer
4. Consumption is calculated automatically

### Vehicle Rates

1. Go to **Fleet Company → Rates**
2. Click **Create** to define rates for a vehicle
3. Set rate per km, per hour, daily, or fixed rates
4. Specify validity period

## Security

Two access groups are created:

- **Fleet Company User**: Can read and create records
- **Fleet Company Manager**: Full access including deletion

## Technical Details

### Models

- `fleet.vehicle.maintenance`: Maintenance records
- `fleet.vehicle.fuel`: Fuel logs
- `fleet.vehicle.rate`: Vehicle rates
- `fleet.maintenance.import`: Excel import wizard

### Dependencies

- `fleet` (Odoo core module)
- `pandas` (Python package for Excel processing)
- `openpyxl` (Python package for Excel file handling)

## License

AGPL-3

## Author

Company

## Support

For issues and questions, please open an issue on GitHub.
