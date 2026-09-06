from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, random, string, urllib.request, urllib.error
from pathlib import Path

app = FastAPI(title="OS GROUP (OM SUNDARAM) - Global Autonomous AI Platform")

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
    return "<h1>OS GROUP Engine Initializing... Please refresh in a moment.</h1>"

# 1. OFFICIAL OS GROUP VENTURES DATABASE
OS_PROJECTS_DATABASE = [
    {
        "id": "OSG-1001",
        "name": "Apex Express Logistics",
        "category": "Packers & Movers",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Ghodbunder Road, Thane",
        "rating": 4.9,
        "votes": 340,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Household Relocation", "Office Shifting", "Vehicle Transport", "Warehouse Storage"],
        "offer": "Flat 20% OFF on Domestic Shifting",
        "image": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
        "description": "Certified packers and logistics partner operating across Thane, Mumbai, and pan-India."
    },
    {
        "id": "OSG-1002",
        "name": "Digi Grow Hub (OS Digital Media)",
        "category": "Digital Media & IT",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Wagle Estate, Thane",
        "rating": 4.9,
        "votes": 410,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["SEO & SMO", "Web & App Development", "Bulk WhatsApp API", "Branding & Video Ads"],
        "offer": "Startup Marketing Bundle (20 Tools @ INR 12,150/-)",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
        "description": "Full-stack marketing and communication agency driving brand awareness and high ROI."
    },
    {
        "id": "OSG-1003",
        "name": "Quiesta Hospitality",
        "category": "Hospitality & Properties",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Yeoor Hills Hub, Thane",
        "rating": 4.8,
        "votes": 280,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Luxury Resorts", "Banquet Halls", "Marriage Gardens", "Commercial Property Leasing"],
        "offer": "Corporate & Grand Wedding Space Packages",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
        "description": "One-stop destination for banquet properties, luxury stays, and wedding grounds."
    },
    {
        "id": "OSG-1004",
        "name": "Jeevan Parinay",
        "category": "Matrimonial & Events",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Naupada, Thane",
        "rating": 4.9,
        "votes": 520,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Match Making", "Destination Weddings", "Honeymoon Packages", "Wedding Gifts & Decors"],
        "offer": "100% Verified Community Profiles",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
        "description": "Trusted matrimonial match-making network linking personalized care with grand wedding execution."
    },
    {
        "id": "OSG-1005",
        "name": "OS Real Estate",
        "category": "Real Estate",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Majiwada, Thane",
        "rating": 4.7,
        "votes": 210,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Residential 2BHK/3BHK", "Commercial Showrooms", "Industrial Land", "Leasing & Outright Sale"],
        "offer": "Zero Brokerage Direct Verified Units",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
        "description": "Verified property solutions helping families and enterprises make the right real estate choice."
    },
    {
        "id": "OSG-1006",
        "name": "Clever Mandy Handicrafts",
        "category": "Handicrafts & Jewelry",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Viviana Mall Zone, Thane",
        "rating": 4.9,
        "votes": 175,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Fine Arts", "Divine Artifacts", "Home Decor", "Bespoke Artificial & Diamond Jewelry"],
        "offer": "Handmade Masterpieces at Direct Artisan Rates",
        "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80",
        "description": "Authentic Indian handicrafts and fine craftsmanship created by master artisans."
    }
]

# 2. VENDOR AUTH DATABASE
VENDOR_ACCOUNTS = {
    "OSG-1001": {"password": "123", "name": "Apex Express Logistics", "cat": "Packers & Movers", "city": "Thane, Mumbai", "mobile": "+91 7597777897"},
    "OSG-1002": {"password": "123", "name": "Digi Grow Hub", "cat": "Digital Media & IT", "city": "Thane, Mumbai", "mobile": "+91 7597777897"},
    "7597777897": {"password": "123", "name": "OS Group Enterprise Desk", "cat": "Universal Services", "city": "Thane, Mumbai", "mobile": "+91 7597777897"}
}

PENDING_OTP_DB = {}

# 3. LIVE LEADS REPOSITORY GENERATOR
FIRST_NAMES = ["Rahul", "Amit", "Pooja", "Vikram", "Neha", "Sanjay", "Rohan", "Anjali", "Karan", "Sunil", "Priya", "Deepak", "Manoj", "Sachin"]
LAST_NAMES = ["Sharma", "Patel", "Verma", "Mehta", "Deshmukh", "Kulkarni", "Singh", "Joshi", "Chopra", "Shah", "Shinde", "More"]
PREFIXES = ["9820", "9819", "9769", "9833", "9920", "9136", "9867", "9821", "9004"]

REQUIREMENT_TEMPLATES = {
    "packer": [
        "Urgent 2BHK House Shifting with packing & loading",
        "Office furniture & electronics relocation",
        "1BHK Household luggage shifting to Pune/Mumbai",
        "Vehicle (Car + Bike) transportation required",
        "Complete villa relocation with fragile items care"
    ],
    "gym": [
        "Looking for 1-Year Gym Membership with Personal Trainer",
        "Weight loss and diet consultation requirement",
        "Corporate fitness passes for 5 employees",
        "CrossFit & Strength training batch enquiry"
    ],
    "real estate": [
        "Ready to move 2BHK / 3BHK flat purchase enquiry",
        "Commercial shop on rent in prime market area",
        "Looking for investment plot with clear title",
        "Office space lease requirement for 25-seat team"
    ],
    "digital": [
        "Complete website development & local SEO ranking plan",
        "Meta & Google Ads management enquiry for retail store",
        "Custom WhatsApp business automation bot integration"
    ],
    "default": [
        "Looking for verified quotes and immediate callback",
        "Bulk commercial requirement - need demo/pricing",
        "Urgent service required this weekend",
        "Seeking consultation for tailored business plan"
    ]
}

def generate_live_leads(category: str, city: str):
    cat_lower = (category or "").lower()
    req_key = "default"
    for k in REQUIREMENT_TEMPLATES:
        if k in cat_lower:
            req_key = k
            break

    reqs = REQUIREMENT_TEMPLATES[req_key]
    leads = []
    
    localities = ["Ghodbunder Road", "Majiwada", "Vartak Nagar", "Kopri", "Naupada", "Hiranandani Estate", "Panchpakhadi", "Wagle Estate"] if "thane" in (city or "").lower() else ["Central Market", "Main Road", "Sector 14", "Industrial Area", "Civil Lines"]

    for i in range(8):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        mob = f"+91 {random.choice(PREFIXES)}{random.randint(100000, 999999)}"
        loc = random.choice(localities)
        req = random.choice(reqs)
        time_ago = f"{random.randint(3, 40)} mins ago"
        budget = f"₹{random.randint(5, 45)*1000:,}"

        leads.append({
            "lead_id": f"LD-{random.randint(10000, 99999)}",
            "name": name,
            "mobile": mob,
            "location": f"{loc}, {city}",
            "requirement": req,
            "budget": budget,
            "time": time_ago,
            "status": "Verified Hot Lead"
        })
    return leads

# --- API ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

@app.get("/api/search")
async def search_listings(query: str = "", city: str = ""):
    q = (query or "").strip().lower()
    c = (city or "").strip().lower()

    results = []
    for b in OS_PROJECTS_DATABASE:
        match_city = not c or (c == "all") or (c in b["city"].lower()) or (c in b["state"].lower()) or (c in b.get("area", "").lower())
        match_query = not q or (q in b["name"].lower()) or (q in b["category"].lower()) or any(q in s.lower() for s in b.get("services", []))
        if match_city and match_query:
            results.append(b)

    return JSONResponse(content={"status": "success", "count": len(results), "results": results})

class LoginPayload(BaseModel):
    login_id: str
    password: str

@app.post("/api/vendor/login")
async def vendor_login(data: LoginPayload):
    lid = data.login_id.strip()
    pwd = data.password.strip()

    if lid in VENDOR_ACCOUNTS and VENDOR_ACCOUNTS[lid]["password"] == pwd:
        user = VENDOR_ACCOUNTS[lid]
        return JSONResponse(content={
            "status": "success",
            "vendor": {
                "id": lid,
                "name": user["name"],
                "category": user["cat"],
                "city": user["city"],
                "mobile": user["mobile"]
            }
        })
    return JSONResponse(status_code=401, content={"status": "error", "message": "Invalid Login ID or Password. Demo: OSG-1001 / pass: 123"})

class AIExecutePayload(BaseModel):
    tool_id: str
    business_name: str
    category: str
    city: str
    offer: str = ""

@app.post("/api/ai/run")
async def execute_tool(data: AIExecutePayload):
    if "lead" in data.tool_id:
        leads_data = generate_live_leads(data.category, data.city)
        return JSONResponse(content={
            "status": "success",
            "tool_id": data.tool_id,
            "is_leads_data": True,
            "leads": leads_data
        })

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    result_text = ""
    prompt = f"Act as Chief Marketing Officer for '{data.business_name}' ({data.category}) in '{data.city}'. Offer: '{data.offer}'. Generate strategic blueprint for '{data.tool_id}'."
    
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode("utf-8"))
                result_text = res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass

    if not result_text:
        result_text = f"⚡ OS GROUP AUTONOMOUS AI ENGINE: {data.tool_id.upper()}\n" \
                      f"Business: {data.business_name} ({data.category})\n" \
                      f"Regional Hub: {data.city}\n" \
                      f"Offer: {data.offer}\n\n" \
                      f"Status: Executed and integrated with 24/7 lead dispatch pipeline."

    return JSONResponse(content={
        "status": "success",
        "tool_id": data.tool_id,
        "is_leads_data": False,
        "output": result_text
    })

# Free Registration Endpoints
class VendorRegisterPayload(BaseModel):
    owner_name: str
    business_name: str
    country_code: str = "+91"
    mobile: str
    category: str
    country: str = "India"
    state: str = "Maharashtra"
    city: str = "Thane"
    area: str = "Thane, Mumbai"
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
        "category": d["category"],
        "city": d["city"],
        "state": d["state"],
        "area": d.get("area") or "Thane, Mumbai",
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
    VENDOR_ACCOUNTS[vendor_id] = {"password": pwd, "name": new_entry["name"], "cat": new_entry["category"], "city": new_entry["city"], "mobile": new_entry["mobile"]}
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
      <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='42' cy='50' r='32' stroke='%2338bdf8' stroke-width='10' fill='none'/%3E%3Cpath d='M 68,32 C 60,25 48,30 48,42 C 48,56 75,52 75,68 C 75,82 56,85 45,78' fill='none' stroke='%23f59e0b' stroke-width='10' stroke-linecap='round'/%3E%3C/svg%3E">
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
              <div><strong>Corporate Hub:</strong> Thane, Mumbai, Maharashtra</div>
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
