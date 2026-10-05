# Test Cases – Cybersecurity Asset Inventory System

| ID | Feature | Input | Expected Result | Status |
|----|---------|-------|-----------------|--------|
| TC-01 | Add asset | Sample asset A101 (HR-PC-01, Workstation, 192.168.1.10, Windows 11, HR, Medium, Secure) | Asset saved, "added successfully" shown | Pass |
| TC-02 | Add multiple assets | Count = 3, sample assets A101–A103 | All 3 stored in `assets.json` | Pass |
| TC-03 | Display assets | Menu option 2 | All assets shown in required format with totals (Total 3, Critical 1, High 1, Medium 1, Vulnerable 1) | Pass |
| TC-04 | Display empty inventory | Menu option 2 with no data | "No assets found in the inventory." | Pass |
| TC-05 | Search by status | Option 5, keyword `vulnerable` | Only Vulnerable assets listed | Pass |
| TC-06 | Search by ID | Option 1, keyword `a103` | Case-insensitive match returns A103 | Pass |
| TC-07 | Search – no match | Option 3, keyword `printer` | "No assets matched" message | Pass |
| TC-08 | Update asset | ID `A102`, new OS `Ubuntu 22.04`, new status `Warning`, rest ENTER | Only OS and status change; others unchanged | Pass |
| TC-09 | Update – ID not found | ID `Z999` | "Asset Z999 not found." | Pass |
| TC-10 | Delete asset | ID `A103`, confirm `y` | Asset removed, file updated | Pass |
| TC-11 | Delete – cancelled | ID `A103`, confirm `n` | "Deletion cancelled", asset kept | Pass |
| TC-12 | Delete – ID not found | ID `Z999` | "Asset Z999 not found." | Pass |
| TC-13 | Security summary | Menu option 6 | Counts by risk, status, type + priority list | Pass |
| TC-14 | Validation – bad Asset ID | `101`, `X1`, `abc` | Rejected, re-prompt: letter + 3+ digits required | Pass |
| TC-15 | Validation – duplicate Asset ID | `A101` when it exists | "Asset ID A101 already exists." | Pass |
| TC-16 | Validation – empty field | Empty Asset Name | "Asset Name cannot be empty." | Pass |
| TC-17 | Validation – invalid asset type | `Laptop` | Rejected; valid types listed | Pass |
| TC-18 | Validation – invalid IP | `999.1.1.1` | "Invalid IPv4 address" | Pass |
| TC-19 | Validation – duplicate IP | `192.168.1.10` already used | "IP … already assigned to A101" | Pass |
| TC-20 | Validation – invalid risk level | `Severe` | Rejected; Low/Medium/High/Critical listed | Pass |
| TC-21 | Validation – invalid status | `Fine` | Rejected; Secure/Warning/Vulnerable listed | Pass |
| TC-22 | Validation – asset count | `abc`, `0` | "Please enter a positive whole number." | Pass |
| TC-23 | Case-insensitive choices | `server`, `CRITICAL` | Normalised to `Server`, `Critical` | Pass |
| TC-24 | Export report | Menu option 7 | `reports/asset_report.txt` created | Pass |
| TC-25 | Import dataset | Menu option 8 | 30 assets imported from `cybersecurity_asset_dataset.csv` | Pass |
| TC-26 | Invalid menu choice | `9`, `x` | "Invalid choice" and menu re-displayed | Pass |
| TC-27 | Persistence | Add asset, exit, restart | Asset still present on restart | Pass |
| TC-28 | Corrupt data file | Invalid JSON in `assets.json` | Warning shown, starts with empty inventory (no crash) | Pass |

Screenshots for TC-01, 03, 05, 08, 10, 13 and 14–22 are in the `screenshots/` folder.
