from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os, json, random, string, urllib.request, urllib.error, re
from pathlib import Path

app = FastAPI(title="OS GROUP - Local Search & Business Marketplace")

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
    return "<h1>Template Loading Error</h1>"

# Preloaded initial verified businesses for instant search (Justdial style)
BUSINESS_DATABASE = [
    {
        "id": "OSG-1001",
        "name": "Apex Strength & Fitness Gym",
        "category": "Gym & Fitness",
        "city": "Jaipur",
        "area": "Malviya Nagar",
        "rating": 4.9,
        "votes": 128,
        "mobile": "+91 9829012345",
        "whatsapp": "+91 9829012345",
        "services": ["CrossFit Training", "Weight Loss Program", "Personal Coaching", "Diet Consultation"],
        "offer": "Flat 20% OFF on Annual Membership",
        "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OSG-1002",
        "name": "Dr. Sharma Multispeciality Dental Clinic",
        "category": "Doctors & Clinics",
        "city": "Jaipur",
        "area": "Vaishali Nagar",
        "rating": 4.8,
        "votes": 94,
        "mobile": "+91 9829054321",
        "whatsapp": "+91 9829054321",
        "services": ["Root Canal Treatment", "Teeth Whitening", "Dental Implants", "Invisible Braces"],
        "offer": "Free First Consultation & X-Ray",
        "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OSG-1003",
        "name": "Royal Heritage Real Estate Developers",
        "category": "Real Estate",
        "city": "Jaipur",
        "area": "Mansarovar",
        "rating": 4.7,
        "votes": 210,
        "mobile": "+91 9829098765",
        "whatsapp": "+91 9829098765",
        "services": ["Luxury 3BHK Flats", "Commercial Retail Shops", "Villa Plots", "Property Valuation"],
        "offer": "Zero Brokerage & Free Registry",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": "OSG-1004",
        "name": "CyberTech AI & Software Labs",
        "category": "IT & Software",
        "city": "Jaipur",
        "area": "C-Scheme",
        "rating": 5.0,
        "votes": 76,
        "mobile": "+91 9829011223",
        "whatsapp": "+91 9829011223",
        "services": ["Custom AI Agent Development", "SaaS Platforms", "Mobile Apps", "SEO & Cloud Hosting"],
        "offer": "Flat 30% Discount for First 10 Startups",
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80"
    }
]

PENDING_OTP_DB = {}
VENDOR_ACCOUNTS = {}

# Banner resolution by niche
def get_banner(cat: str) -> str:
    c = cat.lower()
    if "gym" in c or "fit" in c: return "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80"
    if "doc" in c or "clinic" in c or "dent" in c or "health" in c: return "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1200&q=80"
    if "real" in c or "build" in c or "prop" in c: return "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80"
    if "food" in c or "rest" in c or "cafe" in c: return "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80"
    if "salon" in c or "spa" in c or "beauty" in c: return "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1200&q=80"
    return "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80"

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

# Justdial Search API (Search by Keyword & City)
@app.get("/api/search")
async def search_listings(query: str = "", city: str = "Jaipur"):
    q = query.strip().lower()
    c = city.strip().lower()

    results = []
    for b in BUSINESS_DATABASE:
        match_city = (c in b["city"].lower()) or (c == "all") or not c
        match_query = not q or (q in b["name"].lower()) or (q in b["category"].lower()) or any(q in s.lower() for s in b.get("services", []))
        if match_city and match_query:
            results.append(b)

    return JSONResponse(content={"status": "success", "count": len(results), "results": results})

# Send OTP for Listing Business
class NewBusinessPayload(BaseModel):
    owner_name: str
    business_name: str
    mobile: str
    category: str
    city: str
    area: str = ""
    services: str = ""
    offer: str = ""

@app.post("/api/vendor/send-otp")
async def send_vendor_otp(data: NewBusinessPayload):
    clean_mob = data.mobile.strip().replace(" ", "").replace("-", "")
    otp = str(random.randint(1000, 9999))
    PENDING_OTP_DB[clean_mob] = {"otp": otp, "data": data.dict()}
    return JSONResponse(content={"status": "success", "mobile": clean_mob, "dev_otp": otp})

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
    pwd = f"pass{random.randint(100, 999)}"
    
    new_biz = {
        "id": vendor_id,
        "name": d["business_name"],
        "category": d["category"],
        "city": d["city"],
        "area": d.get("area") or d["city"],
        "rating": 5.0,
        "votes": 1,
        "mobile": d["mobile"],
        "whatsapp": d["mobile"],
        "services": [s.strip() for s in d["services"].split(",") if s.strip()] or ["Premium Services"],
        "offer": d.get("offer") or "Special Discount via OS Group",
        "image": get_banner(d["category"])
    }

    BUSINESS_DATABASE.insert(0, new_biz)
    VENDOR_ACCOUNTS[vendor_id] = {"password": pwd, "biz": new_biz}
    del PENDING_OTP_DB[clean_mob]

    return JSONResponse(content={
        "status": "success",
        "message": "Business successfully listed on OS Group!",
        "vendor_id": vendor_id,
        "password": pwd,
        "business": new_biz
    })
