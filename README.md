# 🚀 FleetPilot: Enterprise Fleet Operations & Logistics Suite for Odoo 18.0

**FleetPilot** is an enterprise-grade fleet management, driver profiling, and logistics coordination addon built from the ground up for **Odoo 18.0**. It streamlines fleet lifecycle monitoring, maintenance schedules, fuel logs, and expense approvals in one unified, high-performance module.

---

## 🌌 Hackathon Value Proposition

Large-scale logistics fleets lose millions annually to **unauthorized vehicle usage, expired operator licenses, unlogged fuel discrepancies, and deferred preventative maintenance**. 

FleetPilot solves this by enforcing **real-time database constraints, automated operational state-machines, and seamless record inter-connectivity** natively within the Odoo 18.0 ecosystem:
- **Preventative Safety**: Hard validation rules block drivers with expired licenses from being dispatched on active trips.
- **Cost Minimization**: Real-time calculators automatically compute per-trip fuel overhead and log maintenance invoices.
- **Audit-Ready Operations**: Multi-stage expense approvals (Draft ➔ Submitted ➔ Approved ➔ Refused) prevent expense leaks.
- **Modern UI**: Clean XML tree, form, and search views, coupled with a customized Action Dashboard, offer high density and visual clarity.

---

## 📂 Project Architecture & File Structure

Here is how your Odoo 18 custom repository is structured:

```text
project/
├── docker-compose.yml              # Multi-container local orchestration (Odoo 18 + PostgreSQL 16)
└── addon/                          # Custom Odoo addons volume mount
    └── fleetpilot/                 # Self-contained Odoo 18 addon module
        ├── __init__.py             # Python module entrypoint
        ├── __manifest__.py         # Odoo module metadata, dependencies, and view declarations
        ├── data/
        │   └── fleetpilot_demo.xml # Automated demo dataset (Vehicles, Drivers, Trips)
        ├── models/                 # Python database models (ORMs)
        │   ├── __init__.py
        │   ├── vehicle.py          # fleetpilot.vehicle (Fuel specs, status, odometer)
        │   ├── driver.py           # fleetpilot.driver (License tracking, contact, states)
        │   ├── trip.py             # fleetpilot.trip (Dispatch workflows & dispatch validation)
        │   ├── maintenance.py      # fleetpilot.maintenance (Schedules, diagnostic reports)
        │   ├── fuel_log.py         # fleetpilot.fuel.log (Direct fuel costs, volume limits)
        │   └── expense.py          # fleetpilot.expense (Multi-state tolls, tax, and repairs)
        ├── security/
        │   └── ir.model.access.csv # Strict security rules (CRUD) for all 6 models
        └── views/                  # XML View definitions
            ├── menus.xml           # Main application parent menus & submenus
            ├── vehicle_views.xml   # Tree, Form, Search & Pivot view for Vehicles
            ├── driver_views.xml    # Tree, Form, and Search views for Drivers
            ├── trip_views.xml      # Trip logistics dispatcher workflows
            ├── maintenance_views.xml # Preventive maintenance scheduler
            ├── fuel_log_views.xml  # Fuel expense optimization dashboard
            ├── expense_views.xml   # Multi-state workflow transitions
            └── dashboard_views.xml # Embedded Client Action Dashboard interface
```

---

## 🐳 Docker Compose Configuration (`docker-compose.yml`)

To run the custom module locally, place this `docker-compose.yml` file in your root `project/` directory. It spins up Odoo 18.0 and a PostgreSQL 16 database, automatically mounting the `./addon` folder as a recognized Odoo addons directory.

```yaml
version: '3.8'

services:
  web:
    image: odoo:18.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      # CRITICAL: Mounts the 'addon' folder into Odoo's custom extra-addons directory
      - ./addon:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    restart: always

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    restart: always

volumes:
  odoo-web-data:
  odoo-db-data:
```

---

## 🚀 How to Run and Install the Addon (Step-by-Step)

### Step 1: Launch Odoo Services
From your VS Code terminal in the root `project/` directory, run:
```bash
docker-compose up -d
```
*This downloads the lightweight images, configures Odoo's database connection, and exposes Odoo on port `8069`.*

---

### Step 2: Access the Web Panel & Create Database
1. Open your browser and navigate to **`http://localhost:8069`**.
2. If prompted, create a new database. Choose an administrator email and password.
3. **Make sure to check the "Demo data" box** if you want Odoo's default contacts and accounts loaded.

---

### Step 3: Activate Developer Mode (Required to install custom modules)
1. Go to **Settings** (using the grid icon in the top left, or the settings block on the dashboard).
2. Scroll to the very bottom.
3. Click **"Activate the developer mode"** (or **"Activate the developer mode with assets"**).

---

### Step 4: Force Odoo to Detect the Custom Addon (The Troubleshooting Trap!)
If you search for `FleetPilot` in the **Apps** list and it does not show up, follow these precise troubleshooting rules:

1. **Click "Update Apps List"**:
   - Go to the **Apps** module.
   - Look at the top horizontal menu bar. Click **"Update Apps List"**.
   - Click the **"Update"** button in the popup dialog.

2. **CRITICAL: Clear the Default search filter!**
   - Odoo's search bar in the "Apps" view has a default filter active called **`Apps`** (indicated by a small colored badge).
   - Because FleetPilot is an operations suite, Odoo might categorize it under general modules rather than standard "Apps".
   - **Click the small `x` next to the `Apps` filter tag** in the search box to remove it.
   - Now, search for `FleetPilot` or `fleetpilot`.

3. **Verify the Directory Nesting**:
   - Ensure Odoo container has access to `__manifest__.py` under exactly `/mnt/extra-addons/fleetpilot/__manifest__.py`.
   - If your folder is nested as `./addon/addon/fleetpilot` or `./addon/fleetpilot/fleetpilot`, Odoo will not see it. Ensure there is only **one** level of nesting: `./addon/fleetpilot/` maps directly to `/mnt/extra-addons/fleetpilot/`.

---

### Step 5: Install & Load Demo Data
1. Once **FleetPilot** appears in your search results, click **Activate** (Install).
2. The page will reload. You will now see the beautiful **FleetPilot** app option in the Odoo Main Menu!
3. Go to FleetPilot. Since the module includes `fleetpilot_demo.xml`, you will find your dashboard, vehicles, and active drivers pre-loaded with mock data so you can present right away!

---

## 🛠️ Python & Odoo 18.0 Development Highlights

Here are the advanced Odoo 18 coding methodologies used in this project that will impress the hackathon judges:

1. **`@api.constrains` for Strict Database Integrity**:
   - Used in `vehicle.py` to prevent entering negative fuel capacities.
   - Used in `trip.py` to check driver license dates and automatically raise a user-friendly `ValidationError` if their license has expired.

2. **Automated Inter-Model Handshakes (State Machines)**:
   - When a dispatch trip's state changes to `dispatched` or `completed`, a custom `write` override trigger modifies the operator status of the vehicle and the driver automatically, keeping the system 100% synchronized without manual clicks.

3. **`ondelete='cascade'` Relational Lifecycles**:
   - Deleting a vehicle or driver records automatically handles maintenance histories and fuel logs cleanly, maintaining solid relational database patterns in PostgreSQL.

4. **Modern UI/UX Configurations in Odoo**:
   - Form views use beautiful, functional `<sheet>` elements with status bars (`<field name="state" widget="statusbar" ...>`) to guide the operator through dispatching workflows.
   - Configured robust searching capabilities using `<search>`, `<group>`, and `<filter>` elements so managers can instantly filter vehicles by status (Active, Maintenance, Out of Service) or search drivers by license status.

---
