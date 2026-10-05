"""
Runs the real program functions with scripted keyboard input and renders
the console transcript as terminal-style PNG screenshots.
"""
import builtins, io, os, sys, tempfile, contextlib
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "src"))
import asset_inventory as ai

TMP = os.path.join(tempfile.mkdtemp(), "assets.json")
ai.DATA_FILE = TMP
OUT = os.path.join(BASE, "screenshots")

def run(menu_choice, func, inputs):
    """Execute func(assets) while echoing scripted input like a terminal."""
    it = iter(inputs)
    buf = io.StringIO()
    def fake_input(prompt=""):
        val = next(it)
        buf.write(f"{prompt}{val}\n")
        return val
    orig = builtins.input
    builtins.input = fake_input
    assets = ai.load_assets(TMP)
    try:
        with contextlib.redirect_stdout(buf):
            func(assets)
    finally:
        builtins.input = orig
    header = f"$ python3 src/asset_inventory.py\n{ai.MENU.strip()}\nEnter your choice: {menu_choice}\n\n"
    return header + buf.getvalue()

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)

def colour(line):
    s = line.strip()
    if s.startswith("[+]"): return (110, 231, 140)
    if s.startswith("[-]"): return (255, 203, 107)
    if s.startswith("[!]") or "[!]" in s[:6]: return (255, 107, 107)
    if s.startswith("$"): return (130, 170, 255)
    if set(s) <= set("=-") and s: return (90, 100, 115)
    if "CYBERSECURITY" in s or "SECURITY SUMMARY" in s: return (255, 255, 255)
    if s.startswith("!"): return (255, 150, 120)
    return (214, 222, 235)

def render(text, name, title, crop_from_menu=False):
    lines = text.rstrip("\n").split("\n")
    lw = max(len(l) for l in lines)
    cw = FONT.getbbox("M")[2]
    lh = 23
    pad = 22
    w = max(lw * cw + pad * 2, 760)
    h = len(lines) * lh + pad * 2 + 38
    img = Image.new("RGB", (w, h), (24, 27, 34))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 36], fill=(44, 49, 60))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([16 + i * 22, 11, 28 + i * 22, 23], fill=c)
    d.text((w // 2 - len(title) * cw // 2, 9), title, font=FONT, fill=(170, 178, 192))
    y = 36 + pad
    for l in lines:
        d.text((pad, y), l, font=BOLD if "CYBERSECURITY" in l else FONT, fill=colour(l))
        y += lh
    img.save(os.path.join(OUT, name))
    print("saved", name, img.size)

# ---- 01 add (sample input from the problem statement) ------------------
add_in = ["3",
  "A101","HR-PC-01","Workstation","192.168.1.10","Windows 11","HR","Medium","Secure",
  "A102","Web-Server","Server","192.168.1.20","Ubuntu","IT","Critical","Vulnerable",
  "A103","Core-Router","Router","192.168.1.1","Cisco IOS","Network","High","Warning"]
render(run("1", ai.add_asset, add_in), "01-add-asset.png", "Add Asset")

# ---- 02 display -------------------------------------------------------
render(run("2", ai.display_assets, []), "02-display-assets.png", "Display Assets")

# ---- 03 search --------------------------------------------------------
render(run("3", ai.search_assets, ["5", "vulnerable"]), "03-search-asset.png", "Search Asset")

# ---- 04 update --------------------------------------------------------
upd_in = ["A102", "", "", "", "Ubuntu 22.04", "", "", "Warning"]
render(run("4", ai.update_asset, upd_in), "04-update-asset.png", "Update Asset")

# ---- 05 delete --------------------------------------------------------
render(run("5", ai.delete_asset, ["A103", "y"]), "05-delete-asset.png", "Delete Asset")

# ---- 06 security summary (re-add a few assets for a richer summary) ---
extra = ai.load_assets(TMP)
extra += [
 dict(asset_id="A104",asset_name="DB-Server",asset_type="Server",ip_address="192.168.1.21",operating_system="Red Hat Linux",department="IT",risk_level="Critical",security_status="Vulnerable"),
 dict(asset_id="A105",asset_name="Core-Switch",asset_type="Switch",ip_address="192.168.1.3",operating_system="Cisco NX-OS",department="Network",risk_level="High",security_status="Warning"),
 dict(asset_id="A106",asset_name="ERP-App",asset_type="Application",ip_address="10.0.0.10",operating_system="SAP",department="Finance",risk_level="Low",security_status="Secure"),
]
ai.save_assets(extra, TMP)
render(run("6", ai.security_summary, []), "06-security-summary.png", "Security Summary")

# ---- 07 input validation ---------------------------------------------
val_in = ["2",
  "101", "X1", "A101", "A110",                       # bad ID, bad ID, duplicate, ok
  "", "Test-PC",                                      # empty name, ok
  "Laptop", "Workstation",                            # bad type, ok
  "999.1.1.1", "192.168.1.10", "192.168.9.9",         # bad IP, duplicate IP, ok
  "Windows 11", "Sales", "Severe", "Low", "Fine", "Secure",
  "abc", "0", "A111", "T-Switch", "Switch", "192.168.9.10", "Cisco IOS", "IT", "High", "Warning"]
render(run("1", ai.add_asset, val_in), "07-input-validation.png", "Input Validation")
