from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os, json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# API Key Render ke Environment Variables se automatically aayegi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    prompt = f"Create a marketing strategy JSON for business: {data.business_name}, {data.category} in {data.city}. Offer: {data.offers}. Keys: tagline, target_audience, brand_tone, welcome_pitch."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    BUSINESS_DB["profile"] = {"info": data.dict(), "brand": json.loads(response.choices[0].message.content)}
    return {"status": "success", "data": BUSINESS_DB["profile"]}

@app.post("/api/generate-content")
async def generate_content():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"Write an Instagram promotional caption and hashtags for {info['business_name']} ({info['category']}). JSON keys: caption, hashtags."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return {"status": "success", "content": json.loads(response.choices[0].message.content)}

@app.post("/api/find-leads")
async def find_leads():
    if "profile" not in BUSINESS_DB:
        return JSONResponse(status_code=400, content={"error": "Pehle register karein."})
    info = BUSINESS_DB["profile"]["info"]
    prompt = f"Generate 5 target leads for {info['category']} in {info['city']}. JSON keys: leads (array of objects with name, contact, interest)."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return {"status": "success", "leads": json.loads(response.choices[0].message.content)}

@app.post("/api/chat-reply")
async def chat_reply(customer_query: str = Form(...)):
    if "profile" not in BUSINESS_DB:
        return {"reply": "Namaste! Hamari service jald live hogi."}
    info = BUSINESS_DB["profile"]["info"]
    system_prompt = f"Tum {info['business_name']} ke customer executive ho. Services: {info['services']}. Offers: {info['offers']}. Helpful Hindi/Hinglish me jawab do."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": customer_query}]
    )
    return {"reply": response.choices[0].message.content}
