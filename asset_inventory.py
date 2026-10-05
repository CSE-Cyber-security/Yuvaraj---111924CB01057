"""
Cybersecurity Asset Inventory System
------------------------------------
A menu-driven console application that lets a security administrator
add, search, update, delete and display the organization's IT assets,
classify them by type / risk level, and generate a security report.

Data is persisted in ../data/assets.json.
"""

import csv
import ipaddress
import json
import os
import re
from datetime import datetime

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "assets.json")
DATASET_CSV = os.path.join(BASE_DIR, "data", "cybersecurity_asset_dataset.csv")
REPORT_FILE = os.path.join(BASE_DIR, "reports", "asset_report.txt")

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Secure", "Warning", "Vulnerable"]

FIELDS = [
    "asset_id", "asset_name", "asset_type", "ip_address",
    "operating_system", "department", "risk_level", "security_status",
]

LINE_EQ = "=" * 41
LINE_DASH = "-" * 41


# ----------------------------------------------------------------------
# Persistence
# ----------------------------------------------------------------------
def load_assets(path=None):
    """Load assets from the JSON file; return [] if missing/corrupt."""
    path = path or DATA_FILE
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("[!] Could not read data file. Starting with empty inventory.")
        return []


def save_assets(assets, path=None):
    """Save assets to the JSON file."""
    path = path or DATA_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(assets, fh, indent=4)


# ----------------------------------------------------------------------
# Validation helpers
# ----------------------------------------------------------------------
def validate_asset_id(value, assets, current_id=None):
    value = value.strip().upper()
    if not re.fullmatch(r"[A-Z]\d{3,}", value):
        return None, "Asset ID must be a letter followed by 3+ digits (e.g. A101)."
    if value != current_id and find_by_id(assets, value):
        return None, f"Asset ID {value} already exists."
    return value, None


def validate_text(value, label):
    value = value.strip()
    if not value:
        return None, f"{label} cannot be empty."
    if len(value) > 50:
        return None, f"{label} must be 50 characters or fewer."
    return value, None


def validate_choice(value, options, label):
    for opt in options:
        if value.strip().lower() == opt.lower():
            return opt, None
    return None, f"{label} must be one of: {', '.join(options)}."


def validate_ip(value, assets, current_id=None):
    value = value.strip()
    try:
        ip = ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError:
        return None, "Invalid IPv4 address (e.g. 192.168.1.10)."
    for a in assets:
        if a["ip_address"] == str(ip) and a["asset_id"] != current_id:
            return None, f"IP {ip} is already assigned to {a['asset_id']}."
    return str(ip), None


def ask(prompt, validator, *args):
    """Prompt repeatedly until the validator accepts the input."""
    while True:
        raw = input(prompt)
        value, error = validator(raw, *args)
        if error:
            print(f"  [!] {error}")
        else:
            return value


# ----------------------------------------------------------------------
# Core operations
# ----------------------------------------------------------------------
def find_by_id(assets, asset_id):
    for a in assets:
        if a["asset_id"].upper() == asset_id.upper():
            return a
    return None


def read_asset(assets, current=None):
    """Collect and validate all fields for a new asset."""
    cid = current["asset_id"] if current else None
    return {
        "asset_id": ask("Asset ID: ", validate_asset_id, assets, cid),
        "asset_name": ask("Asset Name: ", validate_text, "Asset Name"),
        "asset_type": ask(f"Asset Type ({'/'.join(ASSET_TYPES)}): ",
                          validate_choice, ASSET_TYPES, "Asset Type"),
        "ip_address": ask("IP Address: ", validate_ip, assets, cid),
        "operating_system": ask("Operating System: ", validate_text,
                                "Operating System"),
        "department": ask("Department: ", validate_text, "Department"),
        "risk_level": ask(f"Risk Level ({'/'.join(RISK_LEVELS)}): ",
                          validate_choice, RISK_LEVELS, "Risk Level"),
        "security_status": ask(f"Security Status ({'/'.join(STATUSES)}): ",
                               validate_choice, STATUSES, "Security Status"),
    }


def add_asset(assets):
    while True:
        raw = input("Enter number of assets to add: ").strip()
        if raw.isdigit() and int(raw) > 0:
            count = int(raw)
            break
        print("  [!] Please enter a positive whole number.")
    for i in range(1, count + 1):
        print(f"\nAsset {i}")
        assets.append(read_asset(assets))
    save_assets(assets)
    print(f"\n[+] {count} asset(s) added successfully.")


def print_asset(a):
    print(f"Asset ID     : {a['asset_id']}")
    print(f"Asset Name   : {a['asset_name']}")
    print(f"Asset Type   : {a['asset_type']}")
    print(f"IP Address   : {a['ip_address']}")
    print(f"OS           : {a['operating_system']}")
    print(f"Department   : {a['department']}")
    print(f"Risk Level   : {a['risk_level']}")
    print(f"Status       : {a['security_status']}")


def count_summary(assets):
    return {
        "total": len(assets),
        "critical": sum(a["risk_level"] == "Critical" for a in assets),
        "high": sum(a["risk_level"] == "High" for a in assets),
        "medium": sum(a["risk_level"] == "Medium" for a in assets),
        "low": sum(a["risk_level"] == "Low" for a in assets),
        "vulnerable": sum(a["security_status"] == "Vulnerable" for a in assets),
        "warning": sum(a["security_status"] == "Warning" for a in assets),
        "secure": sum(a["security_status"] == "Secure" for a in assets),
    }


def display_assets(assets):
    print(LINE_EQ)
    print(" CYBERSECURITY ASSET INVENTORY")
    print(LINE_EQ)
    if not assets:
        print("No assets found in the inventory.")
        print(LINE_EQ)
        return
    for idx, a in enumerate(assets):
        print_asset(a)
        if idx != len(assets) - 1:
            print(LINE_DASH)
    s = count_summary(assets)
    print(LINE_EQ)
    print(f"Total Assets       : {s['total']}")
    print(f"Critical Assets    : {s['critical']}")
    print(f"High Risk Assets   : {s['high']}")
    print(f"Medium Risk Assets : {s['medium']}")
    print(f"Vulnerable Assets  : {s['vulnerable']}")
    print(LINE_EQ)


def search_assets(assets):
    print("\nSearch by:")
    print("  1. Asset ID        4. Risk Level")
    print("  2. Asset Name      5. Security Status")
    print("  3. Asset Type      6. IP Address")
    choice = input("Choose option (1-6): ").strip()
    keys = {"1": "asset_id", "2": "asset_name", "3": "asset_type",
            "4": "risk_level", "5": "security_status", "6": "ip_address"}
    if choice not in keys:
        print("  [!] Invalid search option.")
        return
    term = input("Enter search keyword: ").strip().lower()
    if not term:
        print("  [!] Search keyword cannot be empty.")
        return
    key = keys[choice]
    results = [a for a in assets if term in a[key].lower()]
    if not results:
        print(f"\n[-] No assets matched '{term}'.")
        return
    print(f"\n[+] {len(results)} asset(s) found:")
    print(LINE_DASH)
    for idx, a in enumerate(results):
        print_asset(a)
        if idx != len(results) - 1:
            print(LINE_DASH)
    print(LINE_DASH)


def update_asset(assets):
    asset_id = input("Enter Asset ID to update: ").strip()
    asset = find_by_id(assets, asset_id)
    if not asset:
        print(f"\n[-] Asset {asset_id.upper()} not found.")
        return
    print("\nCurrent details:")
    print(LINE_DASH)
    print_asset(asset)
    print(LINE_DASH)
    print("Press ENTER to keep the current value.\n")
    cid = asset["asset_id"]

    def keep_or(prompt, validator, *args):
        while True:
            raw = input(prompt)
            if raw.strip() == "":
                return None
            value, error = validator(raw, *args)
            if error:
                print(f"  [!] {error}")
            else:
                return value

    updates = {
        "asset_name": keep_or("New Asset Name: ", validate_text, "Asset Name"),
        "asset_type": keep_or("New Asset Type: ", validate_choice,
                              ASSET_TYPES, "Asset Type"),
        "ip_address": keep_or("New IP Address: ", validate_ip, assets, cid),
        "operating_system": keep_or("New Operating System: ", validate_text,
                                    "Operating System"),
        "department": keep_or("New Department: ", validate_text, "Department"),
        "risk_level": keep_or("New Risk Level: ", validate_choice,
                              RISK_LEVELS, "Risk Level"),
        "security_status": keep_or("New Security Status: ", validate_choice,
                                   STATUSES, "Security Status"),
    }
    for key, value in updates.items():
        if value is not None:
            asset[key] = value
    save_assets(assets)
    print(f"\n[+] Asset {cid} updated successfully.")


def delete_asset(assets):
    asset_id = input("Enter Asset ID to delete: ").strip()
    asset = find_by_id(assets, asset_id)
    if not asset:
        print(f"\n[-] Asset {asset_id.upper()} not found.")
        return
    print()
    print_asset(asset)
    confirm = input("\nAre you sure you want to delete this asset? (y/n): ")
    if confirm.strip().lower() == "y":
        assets.remove(asset)
        save_assets(assets)
        print(f"\n[+] Asset {asset['asset_id']} deleted successfully.")
    else:
        print("\n[-] Deletion cancelled.")


def needs_attention(assets):
    """Assets requiring immediate attention: Critical risk or Vulnerable."""
    return [a for a in assets
            if a["risk_level"] == "Critical"
            or a["security_status"] == "Vulnerable"]


def security_summary(assets):
    s = count_summary(assets)
    print(LINE_EQ)
    print(" SECURITY SUMMARY")
    print(LINE_EQ)
    print(f"Total Assets        : {s['total']}")
    print(LINE_DASH)
    print("By Risk Level")
    print(f"  Critical          : {s['critical']}")
    print(f"  High              : {s['high']}")
    print(f"  Medium            : {s['medium']}")
    print(f"  Low               : {s['low']}")
    print(LINE_DASH)
    print("By Security Status")
    print(f"  Secure            : {s['secure']}")
    print(f"  Warning           : {s['warning']}")
    print(f"  Vulnerable        : {s['vulnerable']}")
    print(LINE_DASH)
    print("By Asset Type")
    for t in ASSET_TYPES:
        print(f"  {t:<17} : {sum(a['asset_type'] == t for a in assets)}")
    print(LINE_DASH)
    urgent = needs_attention(assets)
    print(f"Assets Needing Immediate Attention: {len(urgent)}")
    for a in urgent:
        print(f"  ! {a['asset_id']}  {a['asset_name']:<16} "
              f"{a['risk_level']:<8} {a['security_status']}")
    print(LINE_EQ)


def export_report(assets, path=None):
    """Write a plain-text asset report to reports/asset_report.txt."""
    path = path or REPORT_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    s = count_summary(assets)
    urgent = needs_attention(assets)
    lines = [
        "=" * 100,
        " CYBERSECURITY ASSET REPORT",
        f" Generated on: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "=" * 100,
        "",
        "1. EXECUTIVE SUMMARY",
        "-" * 100,
        f"Total assets            : {s['total']}",
        f"Critical risk assets    : {s['critical']}",
        f"High risk assets        : {s['high']}",
        f"Medium risk assets      : {s['medium']}",
        f"Low risk assets         : {s['low']}",
        f"Secure assets           : {s['secure']}",
        f"Warning assets          : {s['warning']}",
        f"Vulnerable assets       : {s['vulnerable']}",
        f"Need immediate attention: {len(urgent)}",
        "",
        "2. ASSETS BY TYPE",
        "-" * 100,
    ]
    for t in ASSET_TYPES:
        lines.append(f"{t:<14}: {sum(a['asset_type'] == t for a in assets)}")
    lines += ["", "3. ASSETS BY DEPARTMENT", "-" * 100]
    depts = sorted({a["department"] for a in assets})
    for d in depts:
        lines.append(f"{d:<14}: {sum(a['department'] == d for a in assets)}")
    lines += ["", "4. PRIORITY ASSETS (Critical risk OR Vulnerable status)",
              "-" * 100]
    header = (f"{'ID':<6}{'Name':<20}{'Type':<13}{'IP Address':<16}"
              f"{'Dept':<12}{'Risk':<10}{'Status'}")
    lines.append(header)
    for a in sorted(urgent, key=lambda x: RISK_LEVELS.index(x["risk_level"]),
                    reverse=True):
        lines.append(f"{a['asset_id']:<6}{a['asset_name']:<20}"
                     f"{a['asset_type']:<13}{a['ip_address']:<16}"
                     f"{a['department']:<12}{a['risk_level']:<10}"
                     f"{a['security_status']}")
    lines += ["", "5. FULL ASSET INVENTORY", "-" * 100, header]
    for a in assets:
        lines.append(f"{a['asset_id']:<6}{a['asset_name']:<20}"
                     f"{a['asset_type']:<13}{a['ip_address']:<16}"
                     f"{a['department']:<12}{a['risk_level']:<10}"
                     f"{a['security_status']}")
    lines += ["", "6. RECOMMENDATIONS", "-" * 100]
    if urgent:
        lines.append("* Patch and re-scan all Vulnerable assets immediately.")
        lines.append("* Review access controls on Critical-risk assets.")
    if s["warning"]:
        lines.append("* Investigate Warning assets before they escalate.")
    lines.append("* Re-run this report after every remediation cycle.")
    lines.append("=" * 100)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[+] Report exported to {os.path.relpath(path, BASE_DIR)}")


def import_dataset(assets, path=None):
    """Import assets from a CSV dataset, skipping invalid/duplicate rows."""
    path = path or DATASET_CSV
    if not os.path.exists(path):
        print(f"[-] Dataset not found: {path}")
        return
    added = skipped = 0
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            aid, e1 = validate_asset_id(row.get("asset_id", ""), assets)
            ip, e2 = validate_ip(row.get("ip_address", ""), assets)
            t, e3 = validate_choice(row.get("asset_type", ""), ASSET_TYPES, "")
            r, e4 = validate_choice(row.get("risk_level", ""), RISK_LEVELS, "")
            st, e5 = validate_choice(row.get("security_status", ""),
                                     STATUSES, "")
            if any([e1, e2, e3, e4, e5]):
                skipped += 1
                continue
            assets.append({
                "asset_id": aid,
                "asset_name": row["asset_name"].strip(),
                "asset_type": t,
                "ip_address": ip,
                "operating_system": row["operating_system"].strip(),
                "department": row["department"].strip(),
                "risk_level": r,
                "security_status": st,
            })
            added += 1
    save_assets(assets)
    print(f"[+] Import complete: {added} added, {skipped} skipped.")


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------
MENU = """
=========================================
 CYBERSECURITY ASSET INVENTORY SYSTEM
=========================================
 1. Add Asset(s)
 2. Display All Assets
 3. Search Asset
 4. Update Asset
 5. Delete Asset
 6. Security Summary
 7. Export Asset Report
 8. Import Dataset (CSV)
 0. Exit
========================================="""


def main():
    assets = load_assets()
    actions = {
        "1": add_asset, "2": display_assets, "3": search_assets,
        "4": update_asset, "5": delete_asset, "6": security_summary,
        "7": export_report, "8": import_dataset,
    }
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Exiting... Stay secure!")
            break
        action = actions.get(choice)
        if action is None:
            print("  [!] Invalid choice. Please enter a number from 0 to 8.")
            continue
        print()
        action(assets)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting... Stay secure!")
