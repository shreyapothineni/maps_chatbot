import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
import requests
 
load_dotenv()

@tool
def get_directions(origin: str, destination: str) -> str:
    """
    Retrieves step-by-step directions from the origin to the destination using the Google Maps Directions API.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
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
            directions_output = []
            for route_index, route in enumerate(routes):
                steps = route["legs"][0]["steps"]
                directions_output.append(f"Route {route_index + 1} from {origin} to {destination}:\n")
                for i, step in enumerate(steps):
                    instruction = step["html_instructions"]
                    distance = step["distance"]["text"]
                    directions_output.append(f"Step {i + 1}: {instruction} ({distance})")
                directions_output.append("\n" + "="*20 + "\n")
            return "\n".join(directions_output)
        else:
            return "No route found."
    else:
        return f"Error: {response.status_code} - {response.text}"
    
@tool
def get_distance(origin: str, destination: str) -> str:
    """
    Retrieves the distance between the origin and destination
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    distance_url = "https://maps.googleapis.com/maps/api/distance/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }
    response = requests.get(distance_url, params=params)
    if response.status_code == 200:
        distance_data = response.json()
        rows = distance_data.get("rows", [])
        if rows and "elements" in rows[0]:
            output = []
            element = rows[0]["elements"][0]
            if "distance" and "duration" in element:
                distance = (element["distance"]["text"])
                duration = (element["duration"]["text"])
                return f"The distance from {origin} to {destination} is {distance}, and it will take approximately {duration}."

        else:
            return "No route found."
    else:
        return f"Error: {response.status_code} - {response.text}"




llm = ChatNVIDIA(
    model="meta/llama-3.1-405b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
)

llm.bind_tools(tools=[get_directions, get_distance])

response = llm.invoke("How do I get from San Jose University to Santa Clara University")
memory = ConversationBufferMemory() 
print(response.content)
