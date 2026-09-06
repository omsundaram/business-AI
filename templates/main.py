from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, random, string, urllib.request, urllib.error
from pathlib import Path

app = FastAPI(title="OS GROUP (OM SUNDARAM) - Super-App Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

def get_html_content():
    candidates = [
        BASE_DIR / "dashboard.html",
        BASE_DIR / "templates" / "dashboard.html",
        BASE_DIR.parent / "templates" / "dashboard.html",
        BASE_DIR.parent / "dashboard.html"
    ]
    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>OS GROUP Engine Loading...</h1>"

# OFFICIAL OS GROUP VENTURES & PROJECTS DIRECTORY
OS_PROJECTS_DATABASE = [
    {
        "id": "OS-VENTURE-01",
        "name": "Digi Grow Hub (OS Digital Media)",
        "brand": "Digi Grow Hub",
        "category": "Digital Media & IT",
        "city": "Jaipur",
        "state": "Rajasthan",
        "area": "Marudhar Nagar, Ajmer Road",
        "rating": 4.9,
        "votes": 340,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["SEO & SMO", "Web & App Development", "Bulk WhatsApp API", "Branding & Video Ads"],
        "offer": "Startup Marketing Bundle (20 Tools @ INR 12,150/-)",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
        "description": "One-stop gateway for full-stack marketing, digital promotions, and media campaigns."
    },
    {
        "id": "OS-VENTURE-02",
        "name": "Quiesta Hospitality",
        "brand": "Quiesta",
        "category": "Hospitality & Properties",
        "city": "Jaipur",
        "state": "Rajasthan",
        "area": "Marudhar Nagar, Ajmer Road",
        "rating": 4.8,
        "votes": 280,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Hotels & Resorts", "Banquet Halls", "Marriage Gardens", "Property Leasing & Sale"],
        "offer": "Corporate & Grand Wedding Space Packages",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
        "description": "Premium properties, marriage gardens, farmhouses, and revenue-sharing resort chains."
    },
    {
        "id": "OS-VENTURE-03",
        "name": "Jeevan Parinay (Jeewanparinay)",
        "brand": "Jeevan Parinay",
        "category": "Matrimonial & Events",
        "city": "Jaipur",
        "state": "Rajasthan",
        "area": "Ajmer Road",
        "rating": 4.9,
        "votes": 512,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Match Making", "Destination Weddings", "Honeymoon Packages", "Wedding Gifts & Fashion"],
        "offer": "100% Verified Community Profiles",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
        "description": "Trusted matchmaking network linking personal care with professional wedding execution."
    },
    {
        "id": "OS-VENTURE-04",
        "name": "OS Real Estate",
        "brand": "OS Real Estate",
        "category": "Real Estate",
        "city": "Jodhpur",
        "state": "Rajasthan",
        "area": "Bombay Motor Circle",
        "rating": 4.7,
        "votes": 190,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Residential Villas", "Commercial Land", "Industrial Plots", "Rent & Lease Property"],
        "offer": "Zero Brokerage Direct Verified Units",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
        "description": "Authentic property matchmaking helping businesses and families make the right choice."
    },
    {
        "id": "OS-VENTURE-05",
        "name": "Clever Mandy Handicrafts",
        "brand": "Clever Mandy",
        "category": "Handicrafts & Jewelry",
        "city": "Jaipur",
        "state": "Rajasthan",
        "area": "Chitrakoot Yojna",
        "rating": 4.9,
        "votes": 165,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Fine Arts", "Divine Artifacts", "Home Decor", "Bespoke Artificial & Diamond Jewelry"],
        "offer": "Handmade Masterpieces at Direct Artisan Rates",
        "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80",
        "description": "Preserving traditional craftsmanship with modern design aesthetics."
    },
    {
        "id": "OS-VENTURE-06",
        "name": "OS Government & EduTech Hub",
        "brand": "OS EduTech",
        "category": "Government & EduTech",
        "city": "Jaipur",
        "state": "Rajasthan",
        "area": "Chitrakoot Yojna",
        "rating": 5.0,
        "votes": 410,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Atal Tinkering Labs (ATL)", "FoSTaC FSSAI Training", "Smart Metering", "PM-JAY Support"],
        "offer": "CBSE STEM/Robotics Integration",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
        "description": "Pioneering technological education, robotics labs, 3D printing, and public welfare utilities."
    }
]

PENDING_OTP_DB = {}
VENDOR_ACCOUNTS = {}

# Fallback AI Generator
def run_ai_generator(task: str, context: dict) -> str:
    biz = context.get("business_name", "OS Partner")
    sub = context.get("category", "Services")
    city = context.get("city", "Jaipur")
    off = context.get("offer", "Exclusive Deal")

    if task == "graphics":
        return f"""🎨 AI GRAPHIC & BANNER CONCEPTS ({biz}):
Banner 1: "Scale Your {sub} with Confidence in {city}"
- Color Palette: Neon Cyber Blue & Gold (#38bdf8 & #f59e0b)
- Focal Text: "{off}"
- Layout: Modern split card with dual action buttons (Call + WhatsApp).

Banner 2: "Verified Authority & Trusted Service"
- Badge: OS Group Verified Emblem
- Tagline: ENTHRAL | ENGAGE | EXECUTE"""

    elif task == "video":
        return f"""🎬 30-SECOND REEL / VIDEO SCRIPT ({biz}):
[0:00 - 0:05] Hook: "Looking for top-tier {sub} in {city}?" (Dynamic kinetic text)
[0:05 - 0:15] Problem/Solution: Showcase rapid turnaround & "{off}"
[0:15 - 0:25] Authority: "Officially certified by OS GROUP Network."
[0:25 - 0:30] CTA: "Tap the link below to chat on WhatsApp or call instantly!"""

    elif task == "voice":
        return f"""📞 AI VOICE ATTENDANT & AUTO-DIALER PITCH:
"Namaste! Thank you for calling {biz}, your certified {sub} partner in {city}. We are currently running our exclusive promotion: '{off}'. Press 1 to speak with an executive, or press 2 to receive our brochure directly on your WhatsApp. Have a wonderful day!\""""

    elif task == "leads":
        return f"""🎯 HYPER-LOCAL CLIENT LEADS FOR {sub} IN {city}:
1. Commercial Corporate Accounts & Local Retailers in {city} Central Hub
2. High-Intent Walk-in Prospects seeking "{off}"
3. Premium B2B Referrals through OS Group Marketplace Network
4. Inbound Direct WhatsApp Leads channeled through your Storefront"""

    else:
        return f"""🤖 24/7 WHATSAPP & SUPPORT BOT SCRIPT:
"Namaste! Welcome to {biz}. We specialize in {sub} in {city}. Current Offer: {off}. How may we assist your requirement today?\""""

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

@app.get("/api/search")
async def search_listings(query: str = "", city: str = ""):
    q = (query or "").strip().lower()
    c = (city or "").strip().lower()

    results = []
    for b in OS_PROJECTS_DATABASE:
        match_city = not c or (c == "all") or (c in b["city"].lower()) or (c in b["state"].lower())
        match_query = not q or (q in b["name"].lower()) or (q in b["category"].lower()) or any(q in s.lower() for s in b.get("services", []))
        if match_city and match_query:
            results.append(b)

    return JSONResponse(content={"status": "success", "count": len(results), "results": results})

# AI Suite Execution Endpoint
class AIRequestPayload(BaseModel):
    tool: str
    business_name: str
    category: str
    city: str
    offer: str = ""

@app.post("/api/ai/execute")
async def execute_ai_suite(data: AIRequestPayload):
    prompt = f"Act as an Elite AI Marketing Director. Generate {data.tool} for {data.business_name} ({data.category}) in {data.city} with offer {data.offer}."
    
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    result_text = ""
    if api_key:
        for m in ["models/gemini-2.5-flash", "models/gemini-1.5-flash"]:
            url = f"https://generativelanguage.googleapis.com/v1beta/{m}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=12) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and parts[0].get("text"):
                            result_text = parts[0].get("text")
                            break
            except Exception:
                continue

    if not result_text:
        result_text = run_ai_generator(data.tool, data.dict())

    return JSONResponse(content={"status": "success", "tool": data.tool, "output": result_text})

# Vendor Registration
class VendorRegisterPayload(BaseModel):
    owner_name: str
    business_name: str
    country_code: str = "+91"
    mobile: str
    category: str
    country: str = "India"
    state: str = "Rajasthan"
    city: str = "Jaipur"
    area: str = ""
    services: str = ""
    offer: str = ""
    package_name: str = "Gold"
    package_price: int = 35000

@app.post("/api/vendor/send-otp")
async def send_vendor_otp(data: VendorRegisterPayload):
    full_mobile = f"{data.country_code}{data.mobile.strip()}"
    otp = str(random.randint(1000, 9999))
    PENDING_OTP_DB[full_mobile] = {"otp": otp, "data": data.dict()}
    return JSONResponse(content={"status": "success", "mobile": full_mobile, "dev_otp": otp})

class VerifyPayload(BaseModel):
    mobile: str
    otp: str

@app.post("/api/vendor/verify-otp")
async def verify_vendor_otp(data: VerifyPayload):
    clean_mob = data.mobile.strip()
    if clean_mob not in PENDING_OTP_DB:
        return JSONResponse(status_code=400, content={"status": "error", "message": "OTP session expired."})

    record = PENDING_OTP_DB[clean_mob]
    if record["otp"] != data.otp.strip():
        return JSONResponse(status_code=400, content={"status": "error", "message": "Incorrect OTP."})

    d = record["data"]
    vendor_id = f"OSG-{random.randint(2000, 9999)}"
    pwd = f"osg@{random.randint(100, 999)}"

    new_entry = {
        "id": vendor_id,
        "name": d["business_name"],
        "brand": d["business_name"],
        "category": d["category"],
        "city": d["city"],
        "state": d["state"],
        "area": d.get("area") or d["city"],
        "rating": 5.0,
        "votes": 1,
        "mobile": f"{d.get('country_code', '+91')} {d['mobile']}",
        "whatsapp": f"{d.get('country_code', '+91')} {d['mobile']}",
        "services": [s.strip() for s in d["services"].split(",") if s.strip()] or ["Enterprise Solutions"],
        "offer": d.get("offer") or "Verified Partnership Benefit",
        "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
        "description": f"Authorized service provider onboarded under OS GROUP network. Managed by {d['owner_name']}."
    }

    OS_PROJECTS_DATABASE.insert(0, new_entry)
    VENDOR_ACCOUNTS[vendor_id] = {"password": pwd, "biz": new_entry}
    del PENDING_OTP_DB[clean_mob]

    return JSONResponse(content={
        "status": "success",
        "message": "Vendor verified & listed!",
        "vendor_id": vendor_id,
        "password": pwd,
        "business": new_entry
    })

@app.get("/biz/{biz_id}", response_class=HTMLResponse)
async def serve_storefront(biz_id: str):
    biz = next((b for b in OS_PROJECTS_DATABASE if b["id"] == biz_id), OS_PROJECTS_DATABASE[0])
    services_html = "".join([f'<li class="flex items-center gap-2 text-slate-300 text-sm py-1.5"><i class="fa-solid fa-circle-check text-sky-400"></i> {s}</li>' for s in biz["services"]])

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>{biz['name']} - Verified OS GROUP Storefront</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen">
      <header class="border-b border-slate-800 p-4 bg-slate-900 flex justify-between items-center">
        <a href="/" class="text-sky-400 font-bold text-sm"><i class="fa-solid fa-arrow-left mr-2"></i> Back to OS GROUP Directory</a>
        <span class="text-amber-400 text-xs font-bold uppercase"><i class="fa-solid fa-shield-halved mr-1"></i> Certified Merchant</span>
      </header>
      <div class="h-72 relative overflow-hidden">
        <img src="{biz['image']}" class="w-full h-full object-cover filter brightness-50">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent"></div>
        <div class="absolute bottom-6 left-6 max-w-5xl">
          <span class="bg-sky-500/20 text-sky-300 border border-sky-500/30 text-xs px-3 py-1 rounded-full font-bold uppercase">{biz['category']}</span>
          <h1 class="text-3xl sm:text-5xl font-black text-white mt-2 flex items-center gap-3">{biz['name']} <i class="fa-solid fa-circle-check text-sky-400 text-2xl"></i></h1>
          <p class="text-slate-300 text-sm mt-1"><i class="fa-solid fa-location-dot text-amber-400 mr-1"></i> {biz['area']}, {biz['city']}, {biz['state']} &bull; Rating: ★ {biz['rating']} ({biz['votes']} Verified Reviews)</p>
        </div>
      </div>
      <div class="max-w-6xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex flex-wrap gap-4">
            <a href="tel:{biz['mobile']}" class="flex-1 min-w-[140px] bg-sky-600 hover:bg-sky-500 text-white font-bold py-3.5 text-center rounded-xl text-sm transition"><i class="fa-solid fa-phone mr-2"></i> Call Now</a>
            <a href="https://wa.me/{biz['whatsapp'].replace('+','').replace(' ','')}?text=Hi%20{biz['name']}" target="_blank" class="flex-1 min-w-[140px] bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 text-center rounded-xl text-sm transition"><i class="fa-brands fa-whatsapp mr-2"></i> WhatsApp Inquiry</a>
          </div>
          <div class="p-6 bg-amber-500/10 border border-amber-500/30 rounded-2xl">
            <div class="text-xs text-amber-400 font-bold uppercase"><i class="fa-solid fa-tag mr-1"></i> Active Promotional Offer</div>
            <div class="text-xl font-bold text-white mt-1">{biz['offer']}</div>
          </div>
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
            <h3 class="text-lg font-bold text-white mb-4">Services & Capabilities</h3>
            <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">{services_html}</ul>
          </div>
        </div>
        <div>
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
            <h4 class="font-bold text-white border-b border-slate-800 pb-2">Merchant Verification</h4>
            <div class="text-xs text-slate-400 space-y-2">
              <div><strong>Vendor ID:</strong> <span class="text-sky-400">{biz['id']}</span></div>
              <div><strong>CIN Compliance:</strong> U74999RJ2018PTC060766</div>
              <div><strong>Status:</strong> <span class="text-emerald-400 font-bold">100% Verified</span></div>
              <div><strong>Autonomous AI Suite:</strong> Active</div>
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """)
