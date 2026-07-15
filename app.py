import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import json
# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# =====================================
# FastAPI App
# =====================================
app = FastAPI(
    title="AI Product Description Generator",
    version="1.0",
    description="Generate AI-powered product descriptions using Google Gemini"
)
# =====================================
# Request Model
# =====================================
class ProductRequest(BaseModel):
    product_name: str

# =====================================
# Home API
# =====================================
@app.get("/")
def home():
    return {
        "message": "AI Product Description Generator Backend Running Successfully 🚀"
    }

# =====================================
# Health API
# =====================================
@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }

# =====================================
# Generate Product Description API
# =====================================
@app.post("/generate")
def generate_product(data: ProductRequest):
    try:

        prompt = f"""
You are an expert e-commerce copywriter.

Generate complete product marketing content.

Product Name:
{data.product_name}

Return ONLY valid JSON.

{{
  "title": "",
  "description": "",
  "features": [
    "",
    "",
    "",
    "",
    ""
  ],
  "benefits": [
    "",
    "",
    ""
  ],
  "seo_keywords": [
    "",
    "",
    "",
    "",
    ""
  ],
  "call_to_action": ""
}}

Do not return markdown.
Do not return explanations.
Return only JSON.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        return {
            "success": True,
            "product_name": data.product_name,
            "data": result
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid JSON response."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )