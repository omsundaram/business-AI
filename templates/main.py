from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os, json, random, string, urllib.request, urllib.error, re
from pathlib import Path

app = FastAPI(title="OS GROUP - Universal Business AI Ecosystem & Directory")

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
    return "<h1>OS Group Template Loading Error</h1>"

# Master Database
VENDOR_USERS = {}      # {vendor_id: vendor_data_dict}
PENDING_OTP_DB = {}    # {mobile: {"otp": code, "payload": dict}}

# Category to Verified HD Banner mapping
CATEGORY_BANNERS = {
    "tech": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1400&q=80",
    "fitness": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1400&q=80",
    "health": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1400&q=80",
    "realestate": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1400&q=80",
    "food": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1400&q=80",
    "salon": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1400&q=80",
    "education": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1400&q=80",
    "automobile": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=1400&q=80",
    "default": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1400&q=80"
}

def resolve_banner(category_str: str) -> str:
    cat = (category_str or "").lower()
    if any(k in cat for k in ["tech", "software", "it", "web", "ai", "digital"]):
        return CATEGORY_BANNERS["tech"]
    if any(k in cat for k in ["gym", "fitness", "yoga", "crossfit"]):
        return CATEGORY_BANNERS["fitness"]
    if any(k in cat for k in ["health", "clinic", "dental", "doctor", "hospital"]):
        return CATEGORY_BANNERS["health"]
    if any(k in cat for k in ["real estate", "builder", "property", "plot"]):
        return CATEGORY_BANNERS["realestate"]
    if any(k in cat for k in ["food", "restaurant", "cafe", "baker"]):
        return CATEGORY_BANNERS["food"]
    if any(k in cat for k in ["salon", "spa", "beauty", "makeup"]):
        return CATEGORY_BANNERS["salon"]
    if any(k in cat for k in ["education", "school", "coach", "upsc"]):
        return CATEGORY_BANNERS["education"]
    if any(k in cat for k in ["car", "automobile", "bike", "mechanic"]):
        return CATEGORY_BANNERS["automobile"]
    return CATEGORY_BANNERS["default"]

def generate_random_password(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits + "@#$") for _ in range(length))

def generate_vendor_id():
    return f"OSG-{random.randint(100000, 999999)}"

def slugify(text: str) -> str:
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def get_fallback_strategy(biz_dict: dict) -> str:
    biz = biz_dict.get("business_name", "Business")
    owner = biz_dict.get("owner_name", "Founder")
    subcat = biz_dict.get("subcategory", "Enterprise")
    city = biz_dict.get("city", "City")
    state = biz_dict.get("state", "State")
    services = biz_dict.get("services", "Custom Services")
    offers = biz_dict.get("offers", "Special Launch Deal")
    pkg = biz_dict.get("package_name", "Gold")
    price = biz_dict.get("package_price", 35000)

    return f"""🎯 1. WINNING BRAND TAGLINE & POSITIONING:
"{biz} - Smart, Scale-Ready {subcat} Solutions in {city}"
Tagline: "Engineered for Results, Driven by Trust."

👤 2. TARGET CUSTOMER PERSONA:
- Primary Segment: Local business owners, commercial enterprises & retail buyers in {city}, {state}.
- Buying Motivation: Seeking premium {services} with fast delivery and high return on investment.
- Active Offer Trigger: "{offers}"

🚀 3. 30-DAY CLIENT ACQUISITION ROADMAP:
- Week 1 (Foundation): Hyper-local SEO & Meta Geo-Targeted ad launch focused on "{offers}".
- Week 2 (Outreach): Automated WhatsApp and direct discovery campaign targeting 200+ local prospects.
- Week 3 (Conversion): Fast follow-up pipeline with limited-time discount conversion triggers.
- Week 4 (Scale & Referrals): Onboard closed accounts and deploy customer referral incentives.

💬 4. WHATSAPP LAUNCH PITCH:
"Namaste! {owner} yahan {biz} se. Hamari team {city} me fastest {services} provide karti hai. Abhi hamara active offer chal raha hai: '{offers}'. Kya hum aapke saath quick demo discuss kar sakte hain?"

⚙️ PLAN STATUS: {pkg} Plan (INR {price:,}) Active & Verified.
"""

def call_gemini(prompt: str, fallback_data: dict = None) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return get_fallback_strategy(fallback_data) if fallback_data else "System ready."

    for m in ["models/gemini-2.5-flash", "models/gemini-1.5-flash", "models/gemini-pro"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/{m}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return parts[0].get("text", "")
        except Exception:
            continue
    return get_fallback_strategy(fallback_data) if fallback_data else "Processing completed."

class RegistrationPayload(BaseModel):
    owner_name: str
    business_name: str
    mobile: str
    email: str = ""
    whatsapp: str = ""
    category: str = "General"
    subcategory: str = "Business"
    country: str = "India"
    state: str = ""
    city: str = ""
    services: str = ""
    offers: str = ""
    facebook: str = ""
    instagram: str = ""
    youtube: str = ""
    website: str = ""
    package_name: str = "Gold"
    package_price: int = 35000

class OTPVerifyPayload(BaseModel):
    mobile: str
    otp: str

class LoginPayload(BaseModel):
    login_id: str
    password: str

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

# STEP 1: OTP Trigger
@app.post("/api/auth/send-otp")
async def send_registration_otp(data: RegistrationPayload):
    clean_mobile = data.mobile.strip().replace(" ", "").replace("-", "")
    otp_code = str(random.randint(1000, 9999))
    PENDING_OTP_DB[clean_mobile] = {"otp": otp_code, "payload": data.dict()}
    
    print(f"=====================================")
    print(f"[OS GROUP SECURITY] OTP for {clean_mobile}: {otp_code}")
    print(f"=====================================")
    
    return JSONResponse(content={
        "status": "success",
        "message": f"Verification OTP sent to {clean_mobile}.",
        "mobile": clean_mobile,
        "dev_otp": otp_code
    })

# STEP 2: OTP Verification & Auto Business Page Creation
@app.post("/api/auth/verify-otp")
async def verify_otp(data: OTPVerifyPayload):
    clean_mobile = data.mobile.strip().replace(" ", "").replace("-", "")
    if clean_mobile not in PENDING_OTP_DB:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Session expired or invalid mobile."})
    
    record = PENDING_OTP_DB[clean_mobile]
    if record["otp"] != data.otp.strip():
        return JSONResponse(status_code=400, content={"status": "error", "message": "Incorrect OTP."})
    
    vendor_id = generate_vendor_id()
    temp_password = generate_random_password()
    vendor_data = record["payload"]
    slug = slugify(f"{vendor_data['business_name']}-{vendor_data['city']}")
    banner_img = resolve_banner(f"{vendor_data['category']} {vendor_data['subcategory']}")

    # Generate AI Marketing Blueprint & SEO Description
    prompt = f"""
    Act as a World-Class CMO. Generate an actionable Marketing Blueprint for:
    - Business: {vendor_data['business_name']} (Owner: {vendor_data['owner_name']})
    - Niche: {vendor_data['category']} -> {vendor_data['subcategory']}
    - Location: {vendor_data['city']}, {vendor_data['state']}
    - Services: {vendor_data['services']}
    - Offers: {vendor_data['offers']}
    - Package: {vendor_data['package_name']} (Rs.{vendor_data['package_price']})
    """
    strategy = call_gemini(prompt, fallback_data=vendor_data)

    # Master Vendor Record (Includes Justdial Page Data)
    vendor_record = {
        "vendor_id": vendor_id,
        "password": temp_password,
        "mobile": clean_mobile,
        "slug": slug,
        "banner": banner_img,
        "profile": vendor_data,
        "strategy": strategy,
        "verified": True
    }

    VENDOR_USERS[vendor_id] = vendor_record
    VENDOR_USERS[clean_mobile] = vendor_record
    VENDOR_USERS[slug] = vendor_record
    del PENDING_OTP_DB[clean_mobile]

    return JSONResponse(content={
        "status": "success",
        "message": "Vendor verified & Business Profile Page Created!",
        "credentials": {
            "vendor_id": vendor_id,
            "password": temp_password,
            "business_name": vendor_data["business_name"],
            "owner_name": vendor_data["owner_name"],
            "public_page_url": f"/biz/{vendor_id}"
        },
        "strategy": strategy
    })

# STEP 3: Vendor Login
@app.post("/api/auth/login")
async def vendor_login(data: LoginPayload):
    identifier = data.login_id.strip()
    pwd = data.password.strip()

    if identifier in VENDOR_USERS and VENDOR_USERS[identifier]["password"] == pwd:
        user_info = VENDOR_USERS[identifier]
        return JSONResponse(content={
            "status": "success",
            "message": "Login successful!",
            "vendor": {
                "vendor_id": user_info["vendor_id"],
                "profile": user_info["profile"],
                "strategy": user_info["strategy"],
                "public_page_url": f"/biz/{user_info['vendor_id']}"
            }
        })
    return JSONResponse(status_code=401, content={"status": "error", "message": "Invalid Vendor ID/Mobile or Password."})

# ================= PUBLIC JUSTDIAL-STYLE PROFILE PAGE =================
@app.get("/biz/{biz_identifier}", response_class=HTMLResponse)
async def serve_vendor_public_page(biz_identifier: str):
    vendor = VENDOR_USERS.get(biz_identifier)
    if not vendor:
        # Fallback demo vendor if user directly opens
        vendor = {
            "vendor_id": biz_identifier,
            "banner": CATEGORY_BANNERS["tech"],
            "profile": {
                "business_name": "OS Group Verified Enterprise",
                "owner_name": "Executive Partner",
                "category": "Technology & Software",
                "subcategory": "AI & Digital Transformation",
                "city": "Jaipur",
                "state": "Rajasthan",
                "country": "India",
                "mobile": "+91 9876543210",
                "whatsapp": "+91 9876543210",
                "email": "partner@osgroup.com",
                "services": "Autonomous AI Systems, Lead Generation, WhatsApp Bot, Cloud Architecture",
                "offers": "Flat 30% Inaugural Discount",
                "package_name": "Gold"
            },
            "strategy": "Verified by OS Group AI Ecosystem."
        }

    p = vendor["profile"]
    banner = vendor.get("banner", CATEGORY_BANNERS["default"])
    clean_whatsapp = p.get("whatsapp", p.get("mobile", "")).replace("+", "").replace(" ", "").replace("-", "")

    services_list_html = "".join([f'<li class="flex items-center gap-2 text-slate-300 text-sm"><span class="text-sky-400 font-bold">✓</span> {s.strip()}</li>' for s in p.get("services", "Specialized Services").split(",")])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{p['business_name']} - {p['city']} | Verified on OS GROUP Directory</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
      <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}</style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen">
      <!-- Top OS Group Verification Header -->
      <header class="border-b border-slate-800 bg-slate-900/90 py-3 px-4">
        <div class="max-w-6xl mx-auto flex justify-between items-center text-xs">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="text-slate-400">Listed on <strong class="text-sky-400">OS GROUP Marketplace</strong></span>
          </div>
          <a href="/" class="text-sky-400 hover:underline">Explore More Businesses &rarr;</a>
        </div>
      </header>

      <!-- Dynamic Hero Banner with Business Backdrop -->
      <div class="relative h-64 sm:h-80 w-full overflow-hidden">
        <img src="{banner}" alt="{p['business_name']}" class="w-full h-full object-cover object-center filter brightness-50">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent"></div>
        <div class="absolute bottom-6 left-0 right-0 max-w-6xl mx-auto px-4">
          <span class="bg-sky-500/20 text-sky-300 text-xs px-3 py-1 rounded-full border border-sky-500/30 font-semibold uppercase tracking-wider">
            {p['category']} &bull; {p['subcategory']}
          </span>
          <h1 class="text-3xl sm:text-5xl font-black text-white mt-2 flex items-center gap-3">
            {p['business_name']}
            <span title="OS Group Verified" class="text-sky-400 text-2xl">☑</span>
          </h1>
          <p class="text-slate-300 text-sm mt-1 flex items-center gap-2">
            <span>📍 {p['city']}, {p['state']}, {p['country']}</span>
            <span>&bull;</span>
            <span class="text-emerald-400 font-semibold">OS Group Verified Business</span>
          </p>
        </div>
      </div>

      <!-- Main Profile Body: Justdial Layout -->
      <div class="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Left: Details, Services, Offers -->
        <div class="lg:col-span-8 space-y-6">
          <!-- CTA Action Row -->
          <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex flex-wrap gap-3">
            <a href="tel:{p['mobile']}" class="flex-1 min-w-[140px] bg-sky-600 hover:bg-sky-500 text-white font-bold py-3 px-4 rounded-xl text-sm flex items-center justify-center gap-2 transition">
              <span>📞</span> Call Now
            </a>
            <a href="https://wa.me/{clean_whatsapp}?text=Hi%20{p['business_name']},%20I%20saw%20your%20verified%20profile%20on%20OS%20Group.%20I%20want%20details%20about%20your%20services." target="_blank" class="flex-1 min-w-[140px] bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-4 rounded-xl text-sm flex items-center justify-center gap-2 transition">
              <span>💬</span> Chat on WhatsApp
            </a>
          </div>

          <!-- Active Offer Banner -->
          <div class="bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent border border-amber-500/30 p-6 rounded-2xl">
            <div class="text-xs text-amber-400 font-bold uppercase tracking-wider">🔥 Active Promotional Offer</div>
            <div class="text-xl font-bold text-white mt-1">{p['offers']}</div>
            <p class="text-slate-400 text-xs mt-2">Mention OS Group reference when contacting to avail exclusive deal terms.</p>
          </div>

          <!-- Services List -->
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
            <h2 class="text-lg font-bold text-white mb-4">Offered Services & Capabilities</h2>
            <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {services_list_html}
            </ul>
          </div>

          <!-- About Business -->
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
            <h2 class="text-lg font-bold text-white mb-2">About {p['business_name']}</h2>
            <p class="text-slate-300 text-sm leading-relaxed">
              {p['business_name']} is an officially verified provider operating in {p['city']}, {p['state']}, specializing in {p['subcategory']} under the management of {p['owner_name']}. All operations and client workflows are backed by OS Group's Universal Autonomous AI Engine.
            </p>
          </div>
        </div>

        <!-- Right: Inquiry Form & Quick Contact -->
        <div class="lg:col-span-4 space-y-6">
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h3 class="text-base font-bold text-white mb-2">Send Direct Business Inquiry</h3>
            <p class="text-xs text-slate-400 mb-4">Connect directly with {p['business_name']}'s AI desk.</p>
            <form onsubmit="handleInquiry(event)" class="space-y-3">
              <input id="inq_name" required placeholder="Your Name" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-sky-500">
              <input id="inq_mobile" required placeholder="Your Mobile Number" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-sky-500">
              <textarea id="inq_msg" rows="3" placeholder="I am looking for..." class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-sky-500"></textarea>
              <button type="submit" class="w-full py-3 bg-gradient-to-r from-sky-500 to-indigo-600 font-bold text-white text-xs rounded-xl shadow-lg">Submit Requirement</button>
            </form>
            <div id="inq_status" class="text-xs text-emerald-400 mt-3 hidden text-center">Inquiry logged! Business team will reach out.</div>
          </div>

          <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl text-xs space-y-2 text-slate-400">
            <div class="text-white font-bold mb-1">Business Credentials</div>
            <div><strong>Owner:</strong> {p['owner_name']}</div>
            <div><strong>Verification ID:</strong> {vendor.get('vendor_id', 'OSG-VERIFIED')}</div>
            <div><strong>Tier:</strong> {p.get('package_name', 'Gold')} Partner</div>
          </div>
        </div>
      </div>

      <script>
        function handleInquiry(e) {{
          e.preventDefault();
          document.getElementById('inq_status').classList.remove('hidden');
          setTimeout(() => {{
            const mob = document.getElementById('inq_mobile').value;
            const msg = document.getElementById('inq_msg').value;
            window.open('https://wa.me/{clean_whatsapp}?text=' + encodeURIComponent('New lead from OS Group Directory: ' + msg), '_blank');
          }}, 800);
        }}
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Live Actions
@app.post("/api/generate-content")
async def generate_content(biz_name: str = Form("Business"), subcat: str = Form("General"), city: str = Form("City"), offers: str = Form("Offer")):
    prompt = f"Write 2 high-converting Instagram ad copies with 15 viral hashtags for {biz_name} ({subcat}) in {city}. Offer: {offers}."
    output = call_gemini(prompt, fallback_data={"business_name": biz_name, "subcategory": subcat, "city": city, "offers": offers})
    return JSONResponse(content={"status": "success", "content": {"caption": output}})

@app.post("/api/find-leads")
async def find_leads(subcat: str = Form("General"), city: str = Form("City")):
    prompt = f"List 5 targeted prospective client categories and potential local business leads for {subcat} in {city}."
    output = call_gemini(prompt, fallback_data={"subcategory": subcat, "city": city})
    return JSONResponse(content={"status": "success", "leads": output})

@app.post("/api/chat-reply")
async def chat_reply(customer_query: str = Form(...), biz_name: str = Form("OS Group Partner")):
    prompt = f"Tum '{biz_name}' ke AI executive ho. Customer Query: '{customer_query}'. Polite Hinglish me smart business solution do."
    output = call_gemini(prompt, fallback_data={"business_name": biz_name})
    return JSONResponse(content={"reply": output})
