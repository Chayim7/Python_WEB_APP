# AMI Patch Evidence Tracker

> **A modern web application for automating vulnerability patch evidence collection and lifecycle management**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Overview

The **AMI Patch Evidence Tracker** streamlines the patch management workflow by automating evidence collection, vulnerability analysis, and change request documentation. It provides a centralized platform for tracking patch events across DEV, STAGE, and PROD environments with a modern, interactive user interface.

### The Problem It Solves

| Challenge | Solution |
|-----------|----------|
| **Manual evidence collection** takes hours | Automated BEFORE/AFTER scan comparison in seconds |
| **Inconsistent CR documentation** across teams | Standardized, auto-generated CR summaries |
| **No centralized patch tracking** | Single dashboard for all environments |
| **Error-prone vulnerability diffing** | Automated computation with zero human error |
| **Compliance audit gaps** | Complete audit trail with timestamped evidence |

### Core Capabilities

1. **Capture** - Create and manage patch events with metadata (service, environment, AMI ID, date)
2. **Generate** - Produce synthetic BEFORE and AFTER vulnerability scan snapshots
3. **Compute** - Automatically identify fixed vulnerabilities through set difference
4. **Analyze** - Visualize data with interactive charts, tables, and exportable reports
5. **Document** - Generate CR-ready summaries for STAGE and PROD deployments
6. **Enforce** - Control patch lifecycle progression with the State Pattern

> **Note:** This application uses **synthetic data only** for demonstration and development purposes. It does not connect to any real vulnerability scanners or production systems.

---

## Application Views

### 1. Patch Events Dashboard
The central hub for managing all patch events across your infrastructure.

| Feature | Description |
|---------|-------------|
| **Summary Statistics** | Animated counters showing totals by environment and lifecycle phase |
| **Real-time Search** | Instantly filter events by typing keywords |
| **Advanced Filters** | Filter by service, environment, or lifecycle state |
| **Sortable Columns** | Click any column header to sort ascending/descending |
| **Pagination** | Configurable page sizes (5, 10, 25, 50 items) |
| **View Toggle** | Switch between table and card layouts |
| **Quick Actions** | One-click access to details or vulnerability analysis |

### 2. Patch Event Detail
The command center for individual patch events with guided workflow.

| Feature | Description |
|---------|-------------|
| **Metadata Card** | Service, environment, AMI ID, patch date, and notes |
| **Visual Workflow Tracker** | 3-step progress indicator (BEFORE → AFTER → Compute) |
| **Collapsible Sections** | Expandable panels for BEFORE, AFTER, and Fixed vulnerabilities |
| **Severity Badges** | Color-coded counts (Critical, High, Medium, Low) |
| **Lifecycle Controls** | State transition dropdown with validation |
| **CR Generation** | One-click STAGE and PROD change request summaries |

### 3. Vulnerability Analysis
Comprehensive data visualization and reporting dashboard.

| Feature | Description |
|---------|-------------|
| **Interactive Charts** | Radar, Bar/Line, and Donut/Polar charts (Chart.js) |
| **Chart Type Switching** | Toggle between visualization styles |
| **Tabbed Tables** | Fixed, Remaining, Before, and After vulnerability views |
| **Search & Filter** | Real-time filtering by keyword or severity |
| **Sortable Tables** | Click column headers to sort data |
| **Export Options** | Download as CSV or JSON |
| **Report Generation** | Risk score, severity breakdown, and recommendations |
| **Print Support** | Print-friendly formatting |

---

## User Experience

### Modern UI/UX Design
- **Animated backgrounds** with floating orbs and hex grid patterns
- **Glassmorphism** with blur effects and gradient borders
- **3D card effects** with smooth hover animations
- **Responsive layout** for desktop and tablet

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `N` | Create new patch event |
| `D` | Go to Dashboard |
| `A` | Go to Analysis view |
| `?` | Show shortcuts help |
| `Esc` | Close modals |

### Toast Notifications
Real-time, non-intrusive feedback for all user actions.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy ORM |
| **Database** | SQLite (local file) |
| **Templating** | Jinja2 |
| **Frontend** | Tailwind CSS, DaisyUI, Chart.js |
| **Design Pattern** | State Pattern for lifecycle management |

### Patch Lifecycle (State Pattern)

```text
DEV_EVIDENCE_CAPTURED → DEV_VERIFIED → STAGE_CR_READY → STAGE_PATCHED → PROD_CR_READY → PROD_PATCHED → CLOSED
```

The State Pattern enforces valid transitions and prevents promotion without required evidence.

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

## Quick Start Workflow

Follow these steps to experience the full application workflow:

```text
1. CREATE    →  Click "New Patch Event" on the Dashboard
2. CONFIGURE →  Select service, environment, AMI ID, and patch date
3. GENERATE  →  Click "Gen" for BEFORE scan (creates synthetic vulnerabilities)
4. GENERATE  →  Click "Gen" for AFTER scan (simulates post-patch state)
5. COMPUTE   →  Click "Compute" to identify fixed vulnerabilities
6. ANALYZE   →  Click "View Full Analysis" for charts and reports
7. DOCUMENT  →  Generate CR summaries for STAGE and PROD
8. PROMOTE   →  Use lifecycle transitions to move through environments
```

### Lifecycle Rules

- Cannot promote to STAGE/PROD states without DEV evidence
- Cannot close until `PROD_PATCHED` state is reached
- Invalid transitions are blocked with error messages

### Synthetic Data

All CVEs, plugin IDs, AMI IDs, and hosts are **randomly generated synthetic values**. No real vulnerability scanners or production systems are accessed.

---

## Development

### Code Quality

```bash
black app              # Format code
isort app              # Sort imports
flake8 .               # Run linter
```

### Configuration

Create `.flake8` in project root:

```ini
[flake8]
max-line-length = 119
exclude = .git,__pycache__,.venv
```

---

## Business Value

| Benefit | Impact |
|---------|--------|
| **Time Savings** | Evidence collection reduced from hours to minutes |
| **Consistency** | Standardized CR documentation across all teams |
| **Accuracy** | Zero human error in vulnerability diffing |
| **Compliance** | Complete audit trail with timestamped evidence |
| **Visibility** | Single source of truth for all patch events |
| **Scalability** | Handles hundreds of events efficiently |

---

## License

MIT License - See LICENSE file for details.

---

## Author

Developed as part of the OpenClassrooms workplace project requirements.
