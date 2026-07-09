import datetime

class FoodShelfLifePredictor:
    def __init__(self):
        self.food_base_life = {
            "cooked_veg": 12,       
            "cooked_nonveg": 8,     
            "dairy_products": 6,    
            "raw_vegetables": 72,   
            "bakery_bread": 48
        }
    
    def predict_hours_left(self, food_type: str, prep_time_input, current_temp: float) -> dict:
        if food_type not in self.food_base_life:
            return {"status": "error", "message": "Unknown food type"}

        base_life = self.food_base_life[food_type]
        try:
            if isinstance(prep_time_input, str):
                try:
                    prep_time = datetime.datetime.strptime(prep_time_input.strip(), "%Y-%m-%d %H:%M")
                except ValueError:
                    prep_time = datetime.datetime.strptime(prep_time_input.strip(), "%Y-%m-%d %H:%M:%S")
            else:
                prep_time = prep_time_input
                
            current_time = datetime.datetime.now()
            age_hours = (current_time - prep_time).total_seconds() / 3600
        except Exception as e:
            return {"status": "error", "message": f"Invalid date-time object/string. Error: {str(e)}"}
        
        temp_factor = 1.0
        if current_temp > 25:
            temp_factor += (current_temp - 25) * 0.06
        elif current_temp < 10:
            temp_factor = 0.5

        adjusted_total_life = base_life / temp_factor
        remaining_hours = adjusted_total_life - age_hours

        if remaining_hours <= 0:
            return {
                "status": "spoiled",
                "remaining_hours": 0,
                "priority": "CRITICAL",
                "message": "Food is likely spoiled. Do not distribute."
            }
        elif remaining_hours <= 3:
            return {
                "status": "active",
                "remaining_hours": round(remaining_hours, 2),
                "priority": "HIGH",
                "message": "Highly perishable! Must be picked up within 2 hours."
            }
        else:
            return {
                "status": "active",
                "remaining_hours": round(remaining_hours, 2),
                "priority": "NORMAL",
                "message": "Food is safe for distribution."
            }

if __name__ == "__main__":
    predictor = FoodShelfLifePredictor()
    sample_prep_time = datetime.datetime.now() - datetime.timedelta(hours=3)
    formatted_time_str = sample_prep_time.strftime("%Y-%m-%d %H:%M")
    
    print("Testing Predictor Engine with Fixed Validation...")
    print(f"Input Prep Time String: {formatted_time_str}")
    print("-" * 50)
    
    result = predictor.predict_hours_left(
        food_type="cooked_nonveg", 
        prep_time_input=formatted_time_str, 
        current_temp=38.0
    )
    
    import json
    print(json.dumps(result, indent=4))