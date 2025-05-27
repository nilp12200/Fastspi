
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

# Enable CORS for cross-origin requests (update origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your app's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class TranslateRequest(BaseModel):
    q: str
    source: str
    target: str
    format: str = "text"

# Translation endpoint
@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        # Send POST request to LibreTranslate API
        response = requests.post("https://libretranslate.de/translate", json=req.dict(), timeout=10)
        response.raise_for_status()
        return response.json()  # Return the translated text
    except requests.exceptions.RequestException as e:
        # Return error message if something goes wrong
        return JSONResponse(status_code=500, content={"error": str(e)})

