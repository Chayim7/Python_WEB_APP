# AMI Patch Evidence Tracker (Synthetic Data)

## Project Purpose

This application helps patch engineers track AMI-based patch events across environments (DEV → STAGE → PROD) and automatically derive **patch evidence** from synthetic vulnerability scan snapshots.

The main goals are to:

- **Capture** patch events for specific services and environments.
- **Generate** synthetic BEFORE and AFTER scan results (no real systems used).
- **Compute** which vulnerabilities were fixed by a patch (DEV evidence).
- **Analyze** vulnerability data with interactive charts, severity breakdowns, and exportable reports.
- **Summarize** results in a format suitable for change requests (e.g., STAGE/PROD CR text).
- **Enforce** a controlled promotion lifecycle using the **State Pattern**.

This project is built to satisfy the OpenClassrooms workplace project requirements while strictly avoiding any interaction with real company environments or tools.

---

## Key Features

### Modern UI/UX
- **Animated backgrounds** with floating orbs and hex grid patterns
- **Glassmorphism design** with blur effects and gradient borders
- **3D card effects** with hover animations
- **Responsive layout** optimized for desktop and mobile

### Interactive Dashboard
- **Real-time search** across all patch events
- **Sortable columns** (click headers to sort)
- **Pagination** with configurable page sizes (5, 10, 25, 50)
- **View toggle** between table and card layouts
- **Animated counters** for statistics
- **Quick filters** by service, environment, and state

### Vulnerability Analysis View
- **Interactive charts** (Radar, Bar, Donut) with Chart.js
- **Chart type switching** (Bar Line, Donut Polar)
- **Tabbed vulnerability tables** (Fixed, Remaining, Before, After)
- **Search and filter** vulnerabilities by severity
- **Sortable tables** with column headers
- **Export options** (CSV, JSON)
- **Report generation** with severity scoring and risk assessment
- **Copy to clipboard** and print functionality

### Patch Event Detail
- **Visual workflow tracker** showing scan progress (BEFORE → AFTER → Compute)
- **Collapsible sections** for BEFORE, AFTER, and Fixed vulnerabilities
- **Severity badges** with color-coded counts
- **One-click CTA** to view full analysis when evidence is ready
- **State transition controls** with validation

### Keyboard Shortcuts
- `N` - Create new patch event (Dashboard)
- `D` - Go to Dashboard
- `A` - Go to Analysis view
- `?` - Show keyboard shortcuts help
- `Esc` - Close modals

### Toast Notifications
- Real-time feedback for user actions
- Non-intrusive slide-in animations

---

## Synthetic Data Disclaimer (Safety First)

> **Important:** This application uses **synthetic data only**.
>
> - It does **not** connect to any real DEV, STAGE, or PROD environment.
> - It does **not** integrate with or query any of the following (or similar) tools:
>   - Nessus Manager
>   - Trend Micro
>   - Tenable Security Center
>   - ServiceNow (including MID Servers)
>   - Burp Suite
>   - Grafana
>   - Any vulnerability scanner, monitoring tool, or security platform
> - All vulnerabilities, CVEs, plugin IDs, AMI IDs, hosts, and scan results are **fake but realistic in format**.
> - Environments (DEV/STAGE/PROD) and services are treated as **abstract labels only**.

The application is safe to run in isolation: it only reads/writes a local SQLite database.

---

## Architecture & Tech Stack

- **Backend**
  - Python
  - FastAPI (server-rendered HTML views)
  - SQLAlchemy ORM
  - SQLite (local file `patch_tracker.db`)
  - Jinja2 templates
- **Frontend**
  - Tailwind CSS (via CDN)
  - DaisyUI component library (via CDN)
- **Design & Patterns**
  - Object-Oriented design (Service, PatchEvent, ScanSnapshot, Vulnerability, etc.)
  - **State Pattern** for patch lifecycle:
    - DEV_EVIDENCE_CAPTURED → DEV_VERIFIED → STAGE_CR_READY → STAGE_PATCHED → PROD_CR_READY → PROD_PATCHED → CLOSED
- **Key Modules**
  - `app/models.py`  ORM models (Service, PatchEvent, ScanSnapshot, Vulnerability, enums)
  - `app/database.py`  SQLAlchemy engine, session, Base
  - `app/state.py`  lifecycle State Pattern implementation
  - `app/services/synthetic_data.py`  synthetic BEFORE/AFTER scan generation
  - `app/services/diff.py`  fixed vulnerability diff + severity counts
  - `app/web/routes.py`  FastAPI routes and Jinja2 rendering

---

## Project Structure

```text
AMI_Patch_Evidence_Tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entrypoint
│   ├── database.py             # SQLite + SQLAlchemy configuration
│   ├── models.py               # ORM models and enums
│   ├── state.py                # State Pattern for patch lifecycle
│   ├── services/
│   │   ├── __init__.py
│   │   ├── synthetic_data.py   # Synthetic scan generators
│   │   ├── diff.py             # Fixed vuln diff + severity counts
│   │   └── cr_text.py          # CR summary text generation
│   └── web/
│       ├── __init__.py
│       └── routes.py           # Dashboard + patch event + analysis routes
├── templates/
│   ├── base.html               # Shared layout + synthetic data banner
│   ├── dashboard.html          # Interactive dashboard with search/sort/pagination
│   ├── patch_event_detail.html # Patch event detail + workflow + collapsible sections
│   └── vulnerability_analysis.html  # Full analysis view with charts and reports
├── static/                     # Static assets (CSS/JS/images if needed)
├── requirements.txt            # Runtime Python dependencies
└── README.md                   # This file
```

---

## Getting Started

### Prerequisites

- Python **3.10+** (recommended)
- Git
- A terminal (PowerShell / cmd on Windows, or bash/zsh on macOS/Linux)

### 1. Clone the Repository

Replace `<REPO_URL>` with your GitHub URL for this project.

```bash
git clone <REPO_URL>
cd project_6_wingsurf
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the runtime dependencies from `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Install development tools (linting/formatting):

```bash
pip install black isort flake8 flake8-html
```

---

## Running the Web Application

From the project root (with the virtual environment activated):

```bash
python -m uvicorn app.main:app --reload
```

Then open your browser at:

- http://127.0.0.1:8000/

You should see the **Dashboard** screen with:

- A synthetic data disclaimer banner
- An empty patch event list (on first run)
- A "Create Patch Event" button

All data is stored in a local SQLite file (`patch_tracker.db`) created automatically in the project directory on first startup.

---

## Using the Application

### 1. Dashboard

- **Filters**
  - Filter events by:
    - Service (e.g., "Nessus Manager", "Trend Micro", etc.  labels only)
    - Environment (`DEV`, `STAGE`, `PROD`)
    - Lifecycle state (`DEV_EVIDENCE_CAPTURED`, `STAGE_CR_READY`, etc.)
  - Empty / "All" options return all events.
- **Create Patch Event**
  - Click **"Create Patch Event"** to open the patch event detail form.
  
- **Summary stats**
  - The top of the dashboard shows synthetic summary statistics:
    - Total number of patch events
    - Counts by environment (DEV/STAGE/PROD)
    - Counts by lifecycle phase (DEV*, STAGE*, PROD*, CLOSED)
  - These are derived from the same synthetic data stored in SQLite and are meant to
    mimic the style of a production vulnerability/patch overview.

### 2. Creating a Patch Event

On **"Create Patch Event"** page:

- Fill in:
  - **Service**  choose from synthetic service names.
  - **Environment**  one of `DEV`, `STAGE`, `PROD` (labels only).
  - **AMI ID**  e.g., `ami-0syntheticabcd`.
  - **Patch Date**  calendar date.
  - **Notes** (optional)  free-form text.
- Click **"Create Patch Event"**.
- You will be redirected to the **Patch Event Detail** view for the new event.

### 3. Working with Synthetic Scan Snapshots

On a **Patch Event Detail** page (existing event):

- **BEFORE / AFTER snapshot status**
  - The page shows counts of synthetic vulnerabilities:
    - `BEFORE snapshot: N vulnerabilities`
    - `AFTER snapshot:  M vulnerabilities`
- **Generate synthetic BEFORE snapshot**
  - Click **"Generate BEFORE (synthetic)"**.
  - The app:
    - Deletes any previous BEFORE snapshot for this event.
    - Creates a new synthetic snapshot with fake vulnerabilities:
      - CVEs like `CVE-2099-12345`
      - Plugin IDs like `PLUG-10432`
      - Hosts like `dev-synthetic-01`
      - Severities (Critical/High/Medium/Low)
- **Generate synthetic AFTER snapshot**
  - Click **"Generate AFTER (synthetic)"**.
  - The app:
    - If a BEFORE snapshot exists, chooses a random subset of its vulnerabilities
      to simulate **remaining issues**.
    - Otherwise, generates a smaller synthetic set.
  - **Guardrails / UI gating**
    - The **Generate AFTER** button is disabled until a BEFORE snapshot exists.
    - The **Compute fixed vulnerabilities** button is disabled until **both**
      BEFORE and AFTER snapshots exist.
    - On the backend, the `generate-after` route also enforces that a BEFORE
      snapshot must exist and will redirect with a message if called out of
      order.

### 4. Computing Fixed Vulnerabilities (DEV Evidence)

- Once both BEFORE and AFTER snapshots exist:
  - Click **"Compute fixed vulnerabilities"**.
  - The system:
    - Computes the **set difference**: vulnerabilities present in BEFORE but not in AFTER.
    - Marks `dev_evidence_available = True` for this patch event.
- The detail page then displays:
  - A **fixed vulnerabilities table**:
    - Synthetic ID
    - CVE
    - Plugin ID
    - Severity
    - Host
  - **Severity breakdown** for fixed vulnerabilities:
    - Counts of Critical / High / Medium / Low

This computation is performed using synthetic data only and does not require any external scanner or API.

### 5. Lifecycle State Transitions (State Pattern)

Each patch event has a lifecycle, enforced by the **State Pattern**:

```text
DEV_EVIDENCE_CAPTURED
  → DEV_VERIFIED
  → STAGE_CR_READY
  → STAGE_PATCHED
  → PROD_CR_READY
  → PROD_PATCHED
  → CLOSED
```

On the detail page:

- You will see the **current state** as a badge.
- A **"Next state"** dropdown lists only **allowed next states**.
- Click **"Apply transition"** to move the event to the selected next state.

Rules enforced:

- You **cannot** promote toward STAGE/PROD-related states unless **DEV evidence exists** (`dev_evidence_available = True`).
- You **cannot** move to `CLOSED` unless the current state is `PROD_PATCHED`.

If an invalid transition is attempted, the app rolls back the change and shows an error message.

### 6. Generating CR Summaries for STAGE / PROD

Once DEV evidence has been computed for an event, you can generate **synthetic
change request (CR) summaries**:

- **STAGE CR summary**
  - Available when:
    - DEV evidence is available (`dev_evidence_available = True`), and
    - Synthetic BEFORE and AFTER snapshots both exist.
  - Action: click **"Generate STAGE CR summary"** on the detail page.
  - Backend behavior:
    - Recomputes fixed vulnerabilities and severity breakdown.
    - Builds a STAGE CR text block using `app/services/cr_text.py`.
    - Stores it on the patch event for display.

- **PROD CR summary**
  - Available only when the patch event is in one of the later lifecycle states
    (e.g., `STAGE_PATCHED`, `PROD_CR_READY`, `PROD_PATCHED`, `CLOSED`).
  - Also requires synthetic DEV evidence and both BEFORE and AFTER snapshots.
  - Action: click **"Generate PROD CR summary"**.
  - Backend behavior:
    - Uses the same fixed vulnerability diff and severity counts as the STAGE CR.
    - Generates PROD-ready text that assumes STAGE validation is complete and
      PROD rollout is justified (still based on synthetic data).

### 7. Vulnerability Analysis View

Once evidence is computed, click **"View Full Analysis"** to access the comprehensive vulnerability analysis dashboard:

- **Summary Statistics**
  - Animated counters showing BEFORE, AFTER, Fixed, and Remaining vulnerability counts
  - Color-coded severity badges

- **Interactive Charts**
  - **Radar Chart**: Severity distribution comparison (Before vs After)
  - **Bar/Line Chart**: Fixed vulnerabilities by severity (switchable)
  - **Donut/Polar Chart**: Remaining vulnerabilities breakdown (switchable)

- **Tabbed Vulnerability Tables**
  - **Fixed**: Vulnerabilities remediated by the patch
  - **Remaining**: Vulnerabilities still present after patching
  - **Before**: Full BEFORE snapshot data
  - **After**: Full AFTER snapshot data
  - Each table supports:
    - Real-time search filtering
    - Severity filter buttons
    - Sortable columns (click headers)

- **Export Options**
  - **CSV Export**: Download vulnerability data as CSV
  - **JSON Export**: Download as JSON for programmatic use
  - **Print**: Print-friendly view

- **Report Generation**
  - Click **"Generate Report"** to create a comprehensive vulnerability report
  - Includes:
    - Executive summary with risk score (0-100)
    - Severity breakdown with counts and percentages
    - Remediation effectiveness metrics
    - Recommendations based on remaining vulnerabilities
  - Copy to clipboard or print the report

---

## Generating Synthetic Data (Summary)

You never need any real scan results. To exercise the workflow for a patch event:

1. Create a new patch event (typically in **DEV**).
2. On the detail page, click **"Gen"** under BEFORE Scan in the workflow tracker.
3. Click **"Gen"** under AFTER Scan (unlocked after BEFORE is generated).
4. Click **"Compute"** to calculate fixed vulnerabilities and mark DEV evidence.
5. Click **"View Full Analysis"** to explore interactive charts and generate reports.
6. Use lifecycle transitions to conceptually "promote" that patch toward STAGE and PROD.
7. Generate CR summaries for STAGE and PROD environments.

All CVEs, plugin IDs, AMIs, and hosts are **randomly generated synthetic values** that only exist inside this SQLite database.

---

## Linting, Formatting, and flake8-html Report

The project is intended to comply with **PEP 8** and the project requirements using:

- `black` for code formatting
- `isort` for import sorting
- `flake8` + `flake8-html` for linting (you can optionally configure a
  `max-line-length`, for example `119`)

### Sample .flake8 Configuration (optional)

If you want to customize flake8's defaults (for example, to relax line length
to better align with your formatting preferences), create a `.flake8` file at
the project root with at least:

```ini
[flake8]
max-line-length = 119
exclude = .git,__pycache__,.venv
```

### Running Formatters and Linters

From the project root (with virtual environment active):

```bash
# Format code
black app

# Sort imports
isort app

# Run flake8 linting
flake8 .

# Generate flake8-html report
flake8 . --format=html --htmldir=flake8-report
```

- The `flake8-report/` folder will contain an HTML report showing any linting issues.
- For the final project deliverable, this report should show **0 errors**.

---

## Notes for Stakeholders and Reviewers

- **Business value**: Automates the most error-prone and manual part of patch promotion  deriving evidence of which vulnerabilities were fixed in DEV.
- **Safety**: No secrets, no real hostnames, and **no integrations** with production tools. All identifiers are synthetic.
- **Extensibility**: The domain model (PatchEvent, ScanSnapshot, Vulnerability) and State Pattern make it straightforward to extend the lifecycle or add new synthetic data scenarios without touching real systems.

For further details, see:

- UML class diagram in the `docs/` directory.
- User stories, acceptance criteria, and Kanban board in your project management tool (e.g., Jira).
