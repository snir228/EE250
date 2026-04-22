import requests
import json
import geocoder

# WeatherAPI key
WEATHER_API_KEY = '18809380d0854dc1a5a12124260402'

# Return current user location using IP address
def get_current_location():
    g = geocoder.ip('me')
    return g.city

# Get temperature, feels like temperature, weather condition and visibility using weather API
def get_weather(city):
    base_url = "https://api.weatherapi.com/v1/current.json"
    url = base_url + f"?key={WEATHER_API_KEY}&q={city}"  # '?' represents input and '/' is path
    response = requests.get(url)
    
    if response.status_code == 200:
        json_python = json.loads(response.text) # Takes the JSON file as a text and loads it into python data structure
        temp_f = json_python["current"]["temp_f"]
        feelslike_f = json_python["current"]["feelslike_f"]
        weather_cond = json_python["current"]["condition"]["text"]
        visibility = json_python["current"]["vis_miles"]
        return temp_f, feelslike_f, weather_cond, visibility

    else:
        return None
