
# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # import requests
# # from fastapi.middleware.cors import CORSMiddleware

# # app = FastAPI()

# # # Enable CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # Replace with your Android app domain in production
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # class TranslateRequest(BaseModel):
# #     q: str
# #     source: str
# #     target: str
# #     format: str = "text"

# @app.post("/translate")
# def translate(req: TranslateRequest):
#     response = requests.post("https://libretranslate.de/translate", json=req.dict())
#     return response.json()


from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS for all origins (allow access from frontend/Android apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Translation request model
class TranslateRequest(BaseModel):
    q: str         # Text to translate
    source: str    # Source language code
    target: str    # Target language code
    format: str = "text"  # Format: "text" or "html"

# Translation API endpoint
@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        # You can switch this to a self-hosted instance (see below)
        API_URL = "https://translate.argosopentech.com/translate"
        # API_URL = "http://localhost:5000/translate"  # If using local Docker instance

        response = requests.post(API_URL, json=req.dict(), timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
