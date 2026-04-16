import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="weather-service", version="1.0.0")

DEFAULT_CITIES = [
    "Bogota",
    "Cali",
    "Medellin",
    "Cartagena",
    "Barranquilla",
    "Quito",
    "Lima",
    "Mexico City",
    "Madrid",
    "New York",
]

WEATHER_LABELS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Heavy rain showers",
    95: "Thunderstorm",
}


class CitiesResponse(BaseModel):
    cities: list[str]


class WeatherResponse(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature_celsius: float
    wind_speed_kmh: float
    is_day: bool
    weather_code: int
    weather_label: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "weather-service"}


@app.get("/cities", response_model=CitiesResponse)
def get_cities() -> CitiesResponse:
    return CitiesResponse(cities=allowed_cities())


@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str) -> WeatherResponse:
    normalized_city = normalize_city(city)
    if normalized_city not in allowed_cities():
        raise HTTPException(status_code=400, detail="City not allowed in this demo")

    coordinates = await resolve_city_coordinates(normalized_city)
    weather = await fetch_current_weather(coordinates["latitude"], coordinates["longitude"])

    code = weather.get("weather_code", -1)
    return WeatherResponse(
        city=normalized_city,
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
        temperature_celsius=weather.get("temperature_2m"),
        wind_speed_kmh=weather.get("wind_speed_10m"),
        is_day=bool(weather.get("is_day", 0)),
        weather_code=code,
        weather_label=WEATHER_LABELS.get(code, "Unknown"),
    )


async def resolve_city_coordinates(city: str) -> dict[str, float]:
    geocoding_url = os.getenv("OPEN_METEO_GEOCODING_URL", "https://geocoding-api.open-meteo.com/v1/search")
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    data = await http_get_json(geocoding_url, params)

    results = data.get("results") or []
    if not results:
        raise HTTPException(status_code=404, detail="City coordinates not found")

    return {
        "latitude": results[0]["latitude"],
        "longitude": results[0]["longitude"],
    }


async def fetch_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    weather_url = os.getenv("OPEN_METEO_WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m,is_day",
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
    }
    data = await http_get_json(weather_url, params)

    current = data.get("current")
    if not current:
        raise HTTPException(status_code=502, detail="Weather provider returned an invalid response")
    return current


async def http_get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"External API request failed: {exc}") from exc
    return response.json()


def allowed_cities() -> list[str]:
    configured = os.getenv("ALLOWED_CITIES")
    if not configured:
        return DEFAULT_CITIES
    return [city.strip() for city in configured.split(",") if city.strip()]


def normalize_city(city: str) -> str:
    stripped = city.strip()
    city_map = {entry.lower(): entry for entry in allowed_cities()}
    return city_map.get(stripped.lower(), stripped)
