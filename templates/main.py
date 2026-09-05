from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
import os, json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Gemini API Key Render ke Environment Variables se aayegi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model Setup
model = genai.GenerativeModel("gemini-1.5-flash")

BUSINESS_DB = {}

class BusinessRegister(BaseModel):
    business_name: str
    category: str
    city: str
    services: str
    offers: str

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/api/register")
async def register_business(data: BusinessRegister):
    prompt = f"""
    Create a marketing strategy JSON for business:
    Name: {data.business_name}, Category: {data.category}, City: {data.city}, Services: {data.services}, Offer: {data.offers}.
    Return ONLY a valid JSON object with keys: tagline, target_audience, brand_tone, welcome_pitch. No markdown formatting.
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
        return JSONResponse(status_code=400, content={"error": "Pehle register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Write an Instagram promotional caption and hashtags for {info['business_name']} ({info['category']}) in {info['city']}.
    Return ONLY valid JSON with keys: caption, hashtags. No markdown formatting.
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
        return JSONResponse(status_code=400, content={"error": "Pehle register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Generate 5 target potential business/client leads for {info['category']} in {info['city']}.
    Return ONLY valid JSON with format: {{"leads": [{{"name": "...", "contact": "+91 98XXXXXXXX", "interest": "High"}}]}}. No markdown.
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
        return {"reply": "Namaste! Hamari service jald live hogi."}
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"""
    Tum {info['business_name']} ({info['category']}, {info['city']}) ke customer executive ho.
    Services: {info['services']}. Offers: {info['offers']}.
    Customer Query: "{customer_query}"
    Ek helpful, polite Hindi/Hinglish reply do.
    """
    response = model.generate_content(prompt)
    return {"reply": response.text}
