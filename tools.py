import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()

@tool
def get_directions(api_key, origin, destination):
    directions_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }
    response = requests.get(directions_url, params=params)
    
    if response.status_code == 200:
        directions_data = response.json()
        routes = directions_data.get("routes", [])
        if routes:
            for route_index, route in enumerate(routes):
                steps = route["legs"][0]["steps"]
                print(f"Route {route_index + 1} from {origin} to {destination}:\n")
                for i, step in enumerate(steps):
                    instruction = step["html_instructions"]
                    distance = step["distance"]["text"]
                    print(f"Step {i + 1}: {instruction} ({distance})")
                print("\n" + "="*20 + "\n")
        else:
            print("No route found.")
    else:
        print("Error:", response.status_code, response.text)

api_key = os.getenv("GOOGLE_MAPS_API_KEY")

get_directions(api_key, origin, destination)
