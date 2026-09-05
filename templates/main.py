from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os, json, urllib.request, urllib.error
from pathlib import Path

app = FastAPI()

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
    return "<h1>dashboard.html not found</h1>"

def call_gemini(prompt: str) -> str:
    # Har request par live key uthayega
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Render Error: GEMINI_API_KEY environment variable khali (empty) hai."

    # Google ke 3 alag-alag model endpoints
    target_models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    last_debug_info = ""

    for model_name in target_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=25) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except urllib.error.HTTPError as e:
            raw_err = e.read().decode("utf-8")
            last_debug_info = f"HTTP {e.code} on {model_name}: {raw_err}"
            # Agar 404 hai to agla model try karega
            continue
        except Exception as e:
            return f"System Network Error: {str(e)}"

    # Agar teeno fail ho gaye to Google ka exact reason screen par aayega
    return f"Google Rejection Details: {last_debug_info}"

BUSINESS_DB = {}

class FullBusinessRegister(BaseModel):
    owner_name: str = ""
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

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

@app.post("/api/register")
async def register_business(data: FullBusinessRegister):
    prompt = f"""
    Act as an Elite Business CMO. Generate an actionable Marketing & Growth Blueprint for:
    - Business: {data.business_name} (Owner: {data.owner_name})
    - Niche: {data.category} -> {data.subcategory}
    - Location: {data.city}, {data.state}, {data.country}
    - Services: {data.services}
    - Offers: {data.offers}
    - Selected Package: {data.package_name} (Rs.{data.package_price})

    Provide:
    1. Winning Tagline
    2. Target Persona
    3. 30-Day Growth Strategy
    4. WhatsApp Launch Pitch
    """
    output = call_gemini(prompt)
    BUSINESS_DB["profile"] = {"info": data.dict(), "brand": output}
    return JSONResponse(content={"status": "success", "data": BUSINESS_DB["profile"]})

@app.post("/api/generate-content")
async def generate_content():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle form bharkar register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"Write 2 viral Instagram ad copies with 15 trending hashtags for {info['business_name']} ({info['subcategory']}) in {info['city']}. Offer: {info['offers']}."
    output = call_gemini(prompt)
    return JSONResponse(content={"status": "success", "content": {"caption": output}})

@app.post("/api/find-leads")
async def find_leads():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle form bharkar register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"List 5 targeted prospective client categories and potential business leads for {info['subcategory']} in {info['city']}."
    output = call_gemini(prompt)
    return JSONResponse(content={"status": "success", "leads": output})

@app.post("/api/chat-reply")
async def chat_reply(customer_query: str = Form(...)):
    if "profile" not in BUSINESS_DB:
        return JSONResponse(content={"reply": "Namaste! Pehle registration form submit karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"Tum '{info['business_name']}' ke customer executive ho. Services: {info['services']}. Offers: {info['offers']}. Query: '{customer_query}'. Polite Hinglish me reply do."
    output = call_gemini(prompt)
    return JSONResponse(content={"reply": output})
