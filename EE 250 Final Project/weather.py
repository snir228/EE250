import requests
import json
import geocoder

# WeatherAPI key
WEATHER_API_KEY = '18809380d0854dc1a5a12124260402'  # TODO: Replace with your own WeatherAPI key

def get_current_location():
    g = geocoder.ip('me')
    return g.city

def get_weather(city):
    base_url = "https://api.weatherapi.com/v1/current.json"
    url = base_url + f"?key={WEATHER_API_KEY}&q={city}"  # '?' represents input and '/' is path
    response = requests.get(url)
    
    if response.status_code == 200:
        # TODO: Parse the JSON data returned by the API. Extract and process the following information:
        # - Current temperature in Fahrenheit
        # - The "feels like" temperature
        # - Weather condition (e.g., sunny, cloudy, rainy)
        # - Humidity percentage
        # - Wind speed and direction
        # - Atmospheric pressure in mb
        # - UV Index value
        # - Cloud cover percentage
        # - Visibility in miles
        json_python = json.loads(response.text) # Takes the JSON file as a text and loads it into python data structure
        temp_f = json_python["current"]["temp_f"]
        feelslike_f = json_python["current"]["feelslike_f"]
        weather_cond = json_python["current"]["condition"]["text"]
        visibility = json_python["current"]["vis_miles"]
        return temp_f, feelslike_f, weather_cond, visibility

    else:
        # TODO: Implement error handling for common status codes. Provide meaningful error messages based on the status code.
        return None

if __name__ == '__main__':
    # TODO: Prompt the user to input a city name.
    user_city = input("Enter city name: ")
    get_weather(user_city)
    # TODO: Call the 'get_weather' function with the city name provided by the user.
    pass