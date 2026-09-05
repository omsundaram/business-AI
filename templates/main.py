from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os, json, re
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

# Gemini Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
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
    try:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY Render environment variable me set nahi hai!")

        prompt = f"""
        Act as an Elite CMO. Create a high-converting Brand Strategy and Launch Blueprint for:
        - Business: {data.business_name} (Owner: {data.owner_name})
        - Niche: {data.category} -> {data.subcategory}
        - Location: {data.city}, {data.state}, {data.country}
        - Key Services: {data.services}
        - Core Offers: {data.offers}
        - Selected Plan: {data.package_name} (Price: Rs.{data.package_price})

        Generate a clear, professional marketing summary including:
        1. Winning Tagline
        2. Target Audience Persona
        3. Brand Tone
        4. 30-Day Growth Strategy
        5. WhatsApp Welcome Pitch
        """
        response = model.generate_content(prompt)
        ai_text = response.text if hasattr(response, 'text') else str(response)

        BUSINESS_DB["profile"] = {
            "info": data.dict(),
            "brand": ai_text
        }
        return JSONResponse(content={"status": "success", "data": BUSINESS_DB["profile"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/generate-content")
async def generate_content():
    try:
        if "profile" not in BUSINESS_DB:
            return JSONResponse(status_code=400, content={"error": "Pehle registration form complete karein."})
        info = BUSINESS_DB["profile"]["info"]
        prompt = f"Write 2 high-converting Instagram ad copies and 20 trending hashtags for {info['business_name']} ({info['subcategory']}) in {info['city']}. Current Offer: {info['offers']}."
        response = model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "content": {"caption": response.text, "hashtags": ""}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/find-leads")
async def find_leads():
    try:
        if "profile" not in BUSINESS_DB:
            return JSONResponse(status_code=400, content={"error": "Pehle registration form complete karein."})
        info = BUSINESS_DB["profile"]["info"]
        prompt = f"List 5 targeted prospective client types and simulated contact leads for {info['subcategory']} in {info['city']}, {info['state']}."
        response = model.generate_content(prompt)
        return JSONResponse(content={"status": "success", "leads": response.text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/chat-reply")
async def chat_reply(customer_query: str = Form(...)):
    try:
        if "profile" not in BUSINESS_DB:
            return JSONResponse(content={"reply": "Namaste! Hamara AI setup activate ho raha hai."})
        info = BUSINESS_DB["profile"]["info"]
        prompt = f"Tum {info['business_name']} ({info['subcategory']}, {info['city']}) ke executive ho. Services: {info['services']}. Offers: {info['offers']}. Customer Query: '{customer_query}'. Polite Hinglish me jawab do."
        response = model.generate_content(prompt)
        return JSONResponse(content={"reply": response.text})
    except Exception as e:
        return JSONResponse(content={"reply": f"AI Executive busy hai: {str(e)}"})
