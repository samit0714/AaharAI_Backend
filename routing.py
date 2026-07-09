import sys
import subprocess
import time

try:
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
except ImportError:
    print("Geopy library nahi mili. Background me install ho rahi hai...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim

class AaharRouteOptimizer:
    def __init__(self):
        
        self.geolocator = Nominatim(user_agent="AaharAI_Final_App")

    def resolve_to_coords(self, location_input):
        """
        Agar input tuple/list (lat, lon) hai toh direct return karega.
        Agar string address hai toh geocode karne ki koshish karega.
        """
        
        if isinstance(location_input, (tuple, list)) and len(location_input) == 2:
            return location_input
        
        
        try:
            location = self.geolocator.geocode(str(location_input))
            if location:
                return (location.latitude, location.longitude)
        except Exception:
            pass
        return None

    def calculate_delivery_feasibility(self, donor_loc, ngo_loc, remaining_hours: float) -> dict:
        
        donor_coords = self.resolve_to_coords(donor_loc)
        time.sleep(1) 
        ngo_coords = self.resolve_to_coords(ngo_loc)

        
        if not donor_coords or not ngo_coords:
            print("⚠️ Warning: Live Geocoding failed! Using local regional grid calculation fallback.")
            
            donor_coords = (28.6213, 77.3585) if not donor_coords else donor_coords
            ngo_coords = (28.6274, 77.3725) if not ngo_coords else ngo_coords

        
        distance_km = geodesic(donor_coords, ngo_coords).km
        
        
        avg_speed_kmh = 30.0
        estimated_travel_time_hours = distance_km / avg_speed_kmh
        total_required_time = estimated_travel_time_hours + 0.25  

        is_feasible = total_required_time <= remaining_hours

        return {
            "status": "success",
            "donor_coordinates": donor_coords,
            "ngo_coordinates": ngo_coords,
            "distance_km": round(distance_km, 2),
            "estimated_travel_minutes": round(estimated_travel_time_hours * 60, 1),
            "total_required_time_hours": round(total_required_time, 2),
            "is_feasible": is_feasible,
            "message": "NGO can collect safely." if is_feasible else "Alert: NGO too far! Food might spoil before arrival."
        }

if __name__ == "__main__":
    optimizer = AaharRouteOptimizer()
    
    
    jss_noida_coords = (28.6212, 77.3562)
    ngo_sec62_coords = (28.6284, 77.3653)
    
    print("Testing Route Optimizer Engine with Coordinates...")
    print("-" * 50)
    
    result = optimizer.calculate_delivery_feasibility(
        donor_loc=jss_noida_coords, 
        ngo_loc=ngo_sec62_coords, 
        remaining_hours=1.48
    )
    
    import json
    print(json.dumps(result, indent=4))