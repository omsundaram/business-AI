from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os, json
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

def get_html_content():
    file_path = BASE_DIR / "dashboard.html"
    if not file_path.exists():
        file_path = BASE_DIR / "templates" / "dashboard.html"
    if not file_path.exists():
        file_path = BASE_DIR.parent / "templates" / "dashboard.html"
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
BUSINESS_DB = {}

# Enterprise Registration Schema
class FullBusinessRegister(BaseModel):
    owner_name: str
    business_name: str
    mobile: str
    email: str
    whatsapp: str
    category: str
    subcategory: str
    country: str
    state: str
    city: str
    services: str
    offers: str
    facebook: str = ""
    instagram: str = ""
    youtube: str = ""
    website: str = ""
    package_name: str
    package_price: int

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_html_content())

@app.post("/api/register")
async def register_business(data: FullBusinessRegister):
    prompt = f"""
    Create a complete 360-degree Marketing & Growth Blueprint in valid JSON format for:
    - Business: {data.business_name} (Owner: {data.owner_name})
    - Category: {data.category} -> Subcategory: {data.subcategory}
    - Location: {data.city}, {data.state}, {data.country}
    - Services: {data.services}
    - Offers: {data.offers}
    - Selected Package: {data.package_name} (₹{data.package_price})

    Return ONLY a JSON object with keys:
    tagline, target_audience, brand_tone, welcome_pitch, package_execution_plan, growth_milestones
    """
    response = model.generate_content(prompt)
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    try:
        brand_json = json.loads(clean_text)
    except:
        brand_json = {"tagline": response.text}
        
    BUSINESS_DB["profile"] = {"info": data.dict(), "brand": brand_json}
    return {"status": "success", "data": BUSINESS_DB["profile"]}

@app.post("/api/generate-content")
async def generate_content():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle registration karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Write high-converting Instagram caption & hashtags for {info['business_name']} ({info['subcategory']}) in {info['city']}.
    Current Offer: {info['offers']}.
    Return ONLY JSON with keys: caption, hashtags.
    """
    response = model.generate_content(prompt)
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    try:
        content_json = json.loads(clean_text)
    except:
        content_json = {"caption": response.text, "hashtags": ""}
    return {"status": "success", "content": content_json}

@app.post("/api/find-leads")
async def find_leads():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle registration karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Generate 5 prospective business/customer leads for {info['subcategory']} in {info['city']}, {info['state']}.
    Format JSON: {{"leads": [{{"name": "...", "contact": "+91 98XXXXXXXX", "interest": "High", "lead_type": "Direct Consumer"}}]}}
    """
    response = model.generate_content(prompt)
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    try:
        leads_json = json.loads(clean_text)
    except:
        leads_json = {"leads": []}
    return {"status": "success", "leads": leads_json}

@app.post("/api/chat-reply")
async def chat_reply(customer_query: str = Form(...)):
    if "profile" not in BUSINESS_DB:
        return {"reply": "Namaste! Service jald activate hogi."}
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Tum '{info['business_name']}' ({info['subcategory']}, {info['city']}) ke official AI executive ho.
    Services: {info['services']}. Offers: {info['offers']}. WhatsApp Support: {info['whatsapp']}.
    Customer query: "{customer_query}"
    Ek helpful, polite Hindi/Hinglish reply do jo customer ko convert kare.
    """
    response = model.generate_content(prompt)
    return {"reply": response.text}
