# Week 01 – Cybersecurity Asset Inventory System

A menu-driven Python console application that helps a security administrator
**add, search, update, delete and display** an organization's IT assets
(workstations, servers, routers, switches and applications), classify them by
**type** and **risk level**, and quickly find the assets that need immediate attention.

## Features
- Add one or many assets with full input validation
- Display inventory in the required report format with totals
- Search by Asset ID, name, type, risk level, status or IP address
- Update any field (press ENTER to keep the current value)
- Delete with confirmation
- Security summary by risk, status and asset type, plus a **priority list**
  (Critical risk or Vulnerable status)
- Export a text report (`reports/asset_report.txt`)
- Import the sample dataset (`data/cybersecurity_asset_dataset.csv`, 30 assets)
- JSON persistence (`data/assets.json`)

## Validation Rules
| Field | Rule |
|-------|------|
| Asset ID | Letter + 3 or more digits (e.g. `A101`), unique, stored uppercase |
| Asset Name / OS / Department | Not empty, max 50 characters |
| Asset Type | Workstation, Server, Router, Switch, Application |
| IP Address | Valid IPv4, unique across assets |
| Risk Level | Low, Medium, High, Critical |
| Security Status | Secure, Warning, Vulnerable |

Choices are case-insensitive and normalised.

## Project Structure
```
Week-01-Cybersecurity-Asset-Inventory/
├── src/asset_inventory.py                 # main program
├── data/
│   ├── assets.json                        # working inventory (30 assets)
│   └── cybersecurity_asset_dataset.csv    # sample dataset
├── reports/asset_report.txt               # generated asset report
├── tests/test_cases.md                    # 28 test cases
├── tools/                                 # dataset + screenshot generators
├── screenshots/                           # 01–07 output screenshots
└── README.md
```

## How to Run
Requires Python 3.8+ (standard library only).
```bash
cd Week-01-Cybersecurity-Asset-Inventory
python3 src/asset_inventory.py
```
Tip: choose **8** to load the 30-asset dataset, then **7** to export the report.

## Screenshots
| Feature | Screenshot |
|---------|-----------|
| Add asset | ![](screenshots/01-add-asset.png) |
| Display assets | ![](screenshots/02-display-assets.png) |
| Search asset | ![](screenshots/03-search-asset.png) |
| Update asset | ![](screenshots/04-update-asset.png) |
| Delete asset | ![](screenshots/05-delete-asset.png) |
| Security summary | ![](screenshots/06-security-summary.png) |
| Input validation | ![](screenshots/07-input-validation.png) |

## Dataset Overview (30 assets)
| Type | Count | | Risk | Count | | Status | Count |
|------|-------|-|------|-------|-|--------|-------|
| Workstation | 9 | | Critical | 8 | | Secure | 14 |
| Server | 7 | | High | 8 | | Warning | 9 |
| Application | 6 | | Medium | 9 | | Vulnerable | 7 |
| Router | 4 | | Low | 5 | | | |
| Switch | 4 | | | | | | |

12 assets need immediate attention (Critical risk or Vulnerable status).

## Git Commands
```bash
git init
git add .
git commit -m "Week 01: Cybersecurity Asset Inventory System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
