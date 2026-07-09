import sys
import subprocess
import os

# --- AUTOMATIC MANUAL INSTALLER MATRIX ---
# Yeh script check karega aur missing modules ko run-time par manual install karega
required_libraries = {
    "flask": "flask",
    "flask_cors": "flask-cors",
    "geopy": "geopy",
    "gunicorn": "gunicorn"
}

for module_name, pip_name in required_libraries.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"[SYSTEM] {pip_name} nahi mila. Forcefully manually install ho raha hai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        print(f"[SYSTEM] {pip_name} successfully install ho gaya!")

# --- SARE REQUIRED IMPORTS AB SAFE HAIN ---
from flask import Flask, request, jsonify
from flask_cors import CORS
from main_backend import AaharBackendEngine

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing active kiya taaki Shashwat ka frontend block na ho

# Core Backend computation module initiate kiya
backend_engine = AaharBackendEngine()

@app.route('/api/predict_donation', methods=['POST'])
def predict_donation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
            
        # UI Inputs mapping variables
        food_type = data.get("food_type")
        prep_time_str = data.get("prep_time")
        current_temp = float(data.get("current_temp", 30.0))
        quantity = int(data.get("quantity", 1))
        
        # Coordinates input arrays
        donor_coords = tuple(data.get("donor_coords"))
        ngo_coords = tuple(data.get("ngo_coords"))
        
        # Process data with both sub-engines
        result = backend_engine.process_donation_request(
            food_type=food_type,
            prep_time_str=prep_time_str,
            current_temp=current_temp,
            quantity=quantity,
            donor_coords=donor_coords,
            ngo_coords=ngo_coords
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Render system dynamically 'PORT' handle karta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)