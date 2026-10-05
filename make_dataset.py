"""Generates data/cybersecurity_asset_dataset.csv and data/assets.json"""
import csv, json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [
("A101","HR-PC-01","Workstation","192.168.1.10","Windows 11","HR","Medium","Secure"),
("A102","Web-Server","Server","192.168.1.20","Ubuntu 22.04","IT","Critical","Vulnerable"),
("A103","Core-Router","Router","192.168.1.1","Cisco IOS","Network","High","Warning"),
("A104","Finance-PC-01","Workstation","192.168.2.11","Windows 11","Finance","High","Secure"),
("A105","Finance-PC-02","Workstation","192.168.2.12","Windows 10","Finance","High","Warning"),
("A106","DB-Server","Server","192.168.1.21","Red Hat Linux 9","IT","Critical","Warning"),
("A107","Mail-Server","Server","192.168.1.22","Windows Server 2019","IT","High","Secure"),
("A108","File-Server","Server","192.168.1.23","Windows Server 2016","Operations","High","Vulnerable"),
("A109","DNS-Server","Server","192.168.1.24","Debian 12","Network","Critical","Secure"),
("A110","Backup-Server","Server","192.168.1.25","Ubuntu 20.04","IT","Medium","Warning"),
("A111","Edge-Router","Router","192.168.1.2","Juniper Junos","Network","Critical","Vulnerable"),
("A112","Branch-Router","Router","192.168.3.1","MikroTik RouterOS","Network","Medium","Warning"),
("A113","Core-Switch","Switch","192.168.1.3","Cisco NX-OS","Network","High","Secure"),
("A114","Floor1-Switch","Switch","192.168.1.4","Cisco IOS","Network","Low","Secure"),
("A115","Floor2-Switch","Switch","192.168.1.5","HP ProCurve","Network","Medium","Warning"),
("A116","DMZ-Switch","Switch","192.168.1.6","Arista EOS","Network","High","Vulnerable"),
("A117","ERP-App","Application","10.0.0.10","SAP S/4HANA","Finance","Critical","Warning"),
("A118","HR-Portal","Application","10.0.0.11","Apache Tomcat 9","HR","Medium","Secure"),
("A119","CRM-App","Application","10.0.0.12","Salesforce","Sales","Medium","Secure"),
("A120","Intranet-Wiki","Application","10.0.0.13","Confluence","IT","Low","Secure"),
("A121","Payment-Gateway","Application","10.0.0.14","Custom Java App","Finance","Critical","Secure"),
("A122","Legacy-Billing","Application","10.0.0.15","Windows XP App","Finance","Critical","Vulnerable"),
("A123","Dev-PC-01","Workstation","192.168.4.11","Ubuntu 22.04","Engineering","Medium","Secure"),
("A124","Dev-PC-02","Workstation","192.168.4.12","macOS Sonoma","Engineering","Medium","Secure"),
("A125","Reception-PC","Workstation","192.168.5.10","Windows 10","Admin","Low","Warning"),
("A126","Sales-PC-01","Workstation","192.168.6.11","Windows 11","Sales","Low","Secure"),
("A127","Sales-PC-02","Workstation","192.168.6.12","Windows 10","Sales","Medium","Vulnerable"),
("A128","SOC-Workstation","Workstation","192.168.7.10","Kali Linux","Security","High","Secure"),
("A129","VPN-Gateway","Router","192.168.1.7","Fortinet FortiOS","Network","Critical","Warning"),
("A130","Test-Server","Server","192.168.8.20","CentOS 7","Engineering","Low","Vulnerable"),
]
keys = ["asset_id","asset_name","asset_type","ip_address","operating_system","department","risk_level","security_status"]
with open(os.path.join(BASE,"data","cybersecurity_asset_dataset.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(keys); w.writerows(rows)
with open(os.path.join(BASE,"data","assets.json"),"w") as f:
    json.dump([dict(zip(keys,r)) for r in rows], f, indent=4)
print(len(rows),"assets written")
