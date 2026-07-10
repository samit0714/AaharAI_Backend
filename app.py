import sys
import subprocess
import os

# --- PATH RESOLUTION ENGINE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- AUTOMATIC MANUAL INSTALLER MATRIX ---
# FastAPI aur Uvicorn (FastAPI ka server) ko manual list me add kiya hai
required_libraries = {
    "fastapi": "fastapi",
    "pydantic": "pydantic",
    "geopy": "geopy",
    "uvicorn": "uvicorn"
}

for module_name, pip_name in required_libraries.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"[SYSTEM] {pip_name} nahi mila. Forcefully manually install ho raha hai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        print(f"[SYSTEM] {pip_name} successfully install ho gaya!")

# --- FASTAPI SERVER ENGINE CORE ---
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware for FastAPI
from pydantic import BaseModel
from typing import List
from main_backend import AaharBackendEngine

app = FastAPI(title="AaharAI Python Engine")

# CORS Setup: Taaki Node.js server ya frontend isko block na kare
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Real app me yahan front-end ka URL aayega, abhi ke liye public kiya hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AaharBackendEngine()

class DonationRequest(BaseModel):
    food_type: str
    prep_time_str: str
    current_temp: float
    quantity: int
    donor_coords: List[float]
    ngo_coords: List[float]

@app.post("/predict-and-route")
def predict_and_route(req: DonationRequest):
    try:
        result = engine.process_donation_request(
            food_type=req.food_type,
            prep_time_str=req.prep_time_str,
            current_temp=req.current_temp,
            quantity=req.quantity,
            donor_coords=tuple(req.donor_coords),
            ngo_coords=tuple(req.ngo_coords)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:app", host='0.0.0.0', port=port, reload=False)