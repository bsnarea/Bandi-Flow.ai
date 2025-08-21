import requests
import urllib.parse
import datetime

class WeatherTool:
    def __init__(self):
        self.api_key = "9aacc83d647602886d9bbea22bd4f927"  # 발급받은 API 키 입력
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"

    def get_coordinates(self, city, state_code="", country_code=""):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(city)},{state_code},{country_code}&limit=1&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return data["lat"], data["lon"]
        return None

    def get_current_weather(self, city: str) -> str:
        coords = self.get_coordinates(city)
        if not coords:
            return "Error: Could not find coordinates for the city."
        lat, lon = coords
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",  # 섭씨 사용 (imperial로 변경 가능)
            "exclude": "minutely,hourly,alerts"
        }
        headers = {"User-Agent": "OpenWebUI-WeatherScript"}
        response = requests.get(self.base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            return (f"Weather in {city}: {current['weather'][0]['description']}, "
                    f"Temperature: {current['temp']}°C, Feels like: {current['feels_like']}°C")
        return "Error fetching weather data."