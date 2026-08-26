import os
import easyocr
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
GENAI_KEY = os.getenv("GEMINI_API_KEY","API_KEY_HERE")
genai.configure(api_key=GENAI_KEY)
reader = easyocr.Reader(['en'])
@app.get("/")
def home():
    return {"message": "Legal Metrology API Active"}
@app.post("/scan")
async def scan_label(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    results = reader.readtext(image_bytes, detail=0)
    extracted_text = " ".join(results)
    prompt = f"""
    Analyze the following text extracted from a product label under the Legal Metrology (Packaged Commodities) Rules, 2011:
    TEXT: "{extracted_text}" 
    Check for these mandatory declarations:
    1. Name and Address of Manufacturer/Packer/Importer
    2. Country of Origin
    3. Common or Generic Name of Commodity
    4. Net Quantity
    5. Month and Year of Manufacture/Packing/Import
    6. Maximum Retail Price (MRP inclusive of all taxes)
    7. Consumer Care Details (Phone or Email) 
    Provide a structured response:
    - Compliance Status: (Compliant / Non-Compliant / Partial)
    - Extracted Data: List what was found.
    - Missing Fields: List missing mandatory declarations.
    - Summary: Brief explanation of violations if any.
    """
    model = genai.GenerativeModel('gemini-3.6-flash')
    response = model.generate_content(prompt)
    return {
        "extracted_text": extracted_text,
        "analysis": response.text
    }
