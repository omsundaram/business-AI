from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, random, string, urllib.request, urllib.error
from pathlib import Path

app = FastAPI(title="OS GROUP - Autonomous Business Engine & Directory")

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

# 30 Comprehensive Autonomous AI Tools
AI_TOOLS_REGISTRY = {
    # 1. Marketing & Copywriting
    "social_ad": "Generate high-converting Facebook/Instagram ad captions with 20 targeted hashtags",
    "poster_ai": "Dynamic multi-layout visual advertising poster generator with custom themes",
    "seo_meta": "Generate Google SEO Title, Meta Descriptions, and primary keyword strategy",
    "google_ads": "Generate 5 Google Search Ad headlines, descriptions, and callout extensions",
    "email_pitch": "Craft a high-open-rate B2B cold email sequence with persuasive follow-ups",
    "blog_writer": "Generate an SEO-optimized 600-word business thought-leadership article",
    
    # 2. Automation & Communication
    "whatsapp_bot": "Build 24/7 automated WhatsApp inquiry-handling script and flow logic",
    "voice_dialer": "Compose a natural, humanized conversational AI auto-dialer sales pitch",
    "review_responder": "Generate automated 5-star & negative Google review resolution replies",
    "sms_campaign": "Generate high-urgency promotional Bulk SMS variations under 160 characters",
    "lead_qualifier": "AI prompt sequence to ask qualifying budget/timeline questions to prospects",
    "crm_followup": "Automated 3-day, 7-day, and 15-day client re-engagement follow-up sequences",

    # 3. Media, Creative & Video
    "reel_script": "30-second viral Instagram Reel & YouTube Short kinetic video script",
    "product_mockup": "Creative visual banner concepts with lighting, angles, and color palettes",
    "logo_concept": "Corporate brand identity guidelines, font pairings, and color hex codes",
    "festival_banner": "Festive and seasonal promotional offer poster creative blueprint",
    "voiceover_copy": "Professional voiceover narration script for business commercials",
    "influencer_brief": "Direct pitch briefing template for local influencer outreach",

    # 4. Sales & Lead Intelligence
    "lead_extractor": "Hyper-local B2B prospective customer segments and buyer persona roadmap",
    "competitor_spy": "Competitive positioning analysis highlighting strengths over market rivals",
    "pricing_engine": "Dynamic pricing and bundle discount strategy tailored to city tier",
    "proposal_writer": "Executive commercial business proposal with scope of work and ROI pitch",
    "closer_script": "Objection-handling scripts for closing deals over call and WhatsApp",
    "referral_system": "Customer referral program blueprint with incentive structures",

    # 5. Business Operations & Growth
    "growth_blueprint": "30-day customer acquisition roadmap with actionable milestones",
    "market_expansion": "State-wide franchise and branch expansion feasibility blueprint",
    "hiring_spec": "Job descriptions and candidate screening questionnaire for sales staff",
    "faq_generator": "Comprehensive 10-point customer FAQ guide addressing buying hesitation",
    "legal_disclaimer": "Standard Indian commercial service contract clauses and terms outline",
    "pitch_deck": "10-slide startup investor and partner presentation slide-by-slide structure"
}

OS_PROJECTS_DATABASE = [
    {
        "id": "OS-VENTURE-01",
        "name": "Digi Grow Hub (OS Digital Media)",
        "category": "Digital Media & IT",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 4.9,
        "votes": 340,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["SEO & SMO", "Web & App Development", "Bulk WhatsApp API", "Branding & Video Ads"],
        "offer": "Startup Marketing Bundle (20 Tools @ INR 12,150/-)",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OS-VENTURE-02",
        "name": "Quiesta Hospitality",
        "category": "Hospitality & Properties",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 4.8,
        "votes": 280,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Hotels & Resorts", "Banquet Halls", "Marriage Gardens", "Property Leasing & Sale"],
        "offer": "Corporate & Grand Wedding Space Packages",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OS-VENTURE-03",
        "name": "Jeevan Parinay",
        "category": "Matrimonial & Events",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 4.9,
        "votes": 512,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Match Making", "Destination Weddings", "Honeymoon Packages", "Wedding Gifts"],
        "offer": "100% Verified Community Profiles",
        "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OS-VENTURE-04",
        "name": "OS Real Estate",
        "category": "Real Estate",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 4.7,
        "votes": 190,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Residential Villas", "Commercial Land", "Industrial Plots", "Rent & Lease"],
        "offer": "Zero Brokerage Direct Verified Units",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OS-VENTURE-05",
        "name": "Clever Mandy Handicrafts",
        "category": "Handicrafts & Jewelry",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 4.9,
        "votes": 165,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Fine Arts", "Divine Artifacts", "Home Decor", "Bespoke Jewelry"],
        "offer": "Handmade Masterpieces at Artisan Rates",
        "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OS-VENTURE-06",
        "name": "OS Government & EduTech Hub",
        "category": "Government & EduTech",
        "city": "Thane",
        "state": "Maharashtra",
        "area": "Thane, Mumbai",
        "rating": 5.0,
        "votes": 410,
        "mobile": "+91 7597777897",
        "whatsapp": "+91 7597777897",
        "services": ["Atal Tinkering Labs", "FoSTaC FSSAI Training", "Smart Metering", "PM-JAY Support"],
        "offer": "CBSE STEM & Robotics Integration",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80"
    }
]

PENDING_OTP_DB = {}
VENDOR_ACCOUNTS = {}

def fallback_generator(tool_id: str, context: dict) -> str:
    biz = context.get("business_name", "OS Partner")
    sub = context.get("category", "Services")
    city = context.get("city", "Thane, Mumbai")
    off = context.get("offer", "Exclusive Promotion")
    task_desc = AI_TOOLS_REGISTRY.get(tool_id, "Business Solution")

    return f"""⚡ OS GROUP AUTONOMOUS AI ENGINE: {tool_id.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 Business Target: {biz} ({sub})
📍 Regional Hub: {city}
🏷️ Active Hook/Offer: "{off}"
⚙️ Operational Objective: {task_desc}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 1. STRATEGIC DELIVERABLE & ACTION SPECIFICATION:
- Executive Summary: Engineered to generate instant lead acquisition for {biz} across {city}.
- Positioning Statement: "Redefining {sub} with verified excellence and unmatched value."

📋 2. EXECUTION CONTENT & OPERATIONAL FLOW:
- Primary Hook: "Don't settle for average {sub} in {city}. Benefit from our verified guarantee!"
- Core Conversion Pitch: Avail "{off}" exclusively when booking through OS Group.
- Call to Action: Direct WhatsApp dispatch and automated call desk confirmation active.

🚀 3. DEPLOYMENT PROTOCOL:
- Status: 100% Ready for live broadcast.
- Multi-Channel Sync: Synced with your OS GROUP verified merchant profile.
"""

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

class AIExecutePayload(BaseModel):
    tool_id: str
    business_name: str
    category: str
    city: str
    offer: str = ""

@app.post("/api/ai/run")
async def execute_tool(data: AIExecutePayload):
    prompt = f"Act as an expert Chief Marketing Officer and Business Architect. Execute tool '{data.tool_id}' ({AI_TOOLS_REGISTRY.get(data.tool_id, '')}) for '{data.business_name}' ({data.category}) in '{data.city}'. Incorporate current offer '{data.offer}'. Format cleanly with actionable sections."

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
        result_text = fallback_generator(data.tool_id, data.dict())

    return JSONResponse(content={"status": "success", "tool_id": data.tool_id, "output": result_text})

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
        "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80"
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
              <div><strong>Status:</strong> <span class="text-emerald-400 font-bold">100% Verified</span></div>
              <div><strong>Autonomous AI Suite:</strong> Active</div>
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """)
