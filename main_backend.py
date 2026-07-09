import datetime
import json
from predictor import FoodShelfLifePredictor
from routing import AaharRouteOptimizer

class AaharBackendEngine:
    def __init__(self):
        self.predictor = FoodShelfLifePredictor()
        self.router = AaharRouteOptimizer()

    
    def process_donation_request(self, food_type: str, prep_time_str: str, current_temp: float, quantity: int, donor_coords: tuple, ngo_coords: tuple) -> dict:
        print(f"\n[SYSTEM] New food donation request received for {quantity} people. Processing...")

        
        life_result = self.predictor.predict_hours_left(
            food_type=food_type, 
            prep_time_input=prep_time_str, 
            current_temp=current_temp
        )

        if life_result["status"] == "error":
            return life_result

        if life_result["status"] == "spoiled":
            return {
                "donation_status": "REJECTED",
                "reason": "Food is spoiled.",
                "food_quantity_people": quantity, 
                "shelf_life_analysis": life_result,
                "routing_analysis": None
            }

        
        remaining_hours = life_result["remaining_hours"]
        route_result = self.router.calculate_delivery_feasibility(
            donor_loc=donor_coords, 
            ngo_loc=ngo_coords, 
            remaining_hours=remaining_hours
        )

        if route_result["status"] == "success" and route_result["is_feasible"]:
            decision = "APPROVED_FOR_PICKUP"
        else:
            decision = "REJECTED_TOO_FAR"

        return {
            "donation_status": decision,
            "food_quantity_people": quantity, 
            "shelf_life_analysis": life_result,
            "routing_analysis": route_result,
            "timestamp": str(datetime.datetime.now())
        }

if __name__ == "__main__":
    backend = AaharBackendEngine()
    
    two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)
    prep_time_mock = two_hours_ago.strftime("%Y-%m-%d %H:%M")
    
    jss_noida = (28.6212, 77.3562)
    ngo_location = (28.6284, 77.3653)

    
    final_output = backend.process_donation_request(
        food_type="cooked_veg",
        prep_time_str=prep_time_mock,
        current_temp=35.0,
        quantity=50, 
        donor_coords=jss_noida,
        ngo_coords=ngo_location
    )
    
    print("\n--- FINAL BACKEND RESPONSE WITH QUANTITY ---")
    print(json.dumps(final_output, indent=4))