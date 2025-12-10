#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aviation Weather API Test Script
Tests both OpenWeather and Aviation Weather APIs
"""

import requests
import json
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Test coordinates (New York JFK Airport)
LAT = 40.6413
LON = -73.7781
AIRPORT_CODE = "KJFK"

print("=" * 60)
print("Aviation Weather API Test")
print("=" * 60)
print()

# Test 1: OpenWeather API
print("1. Testing OpenWeather API...")
OPENWEATHER_KEY = os.getenv('OPEN_WEATHER_API_KEY', '')
if not OPENWEATHER_KEY:
    print("   ⚠️  OPEN_WEATHER_API_KEY not found in .env")
    print()
else:
    openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_KEY}&units=metric"

    try:
        response = requests.get(openweather_url, timeout=5)
        response.raise_for_status()
        weather_data = response.json()

        print(f"   ✅ Status: {response.status_code}")
        print(f"   🌡️  Temperature: {weather_data['main']['temp']}°C")
        print(f"   💧 Humidity: {weather_data['main']['humidity']}%")
        print(f"   🌬️  Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"   ☁️  Conditions: {weather_data['weather'][0]['description']}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()

# Test 2: Aviation Weather API (METAR)
print("2. Testing Aviation Weather API (METAR)...")
aviation_metar_url = f"https://aviationweather.gov/api/data/metar?ids={AIRPORT_CODE}&format=json"

try:
    response = requests.get(aviation_metar_url, timeout=5)
    response.raise_for_status()
    metar_data = response.json()

    if metar_data:
        print(f"   ✅ Status: {response.status_code}")
        print(f"   🛩️  Airport: {metar_data[0].get('icaoId', 'N/A')}")
        print(f"   🌡️  Temperature: {metar_data[0].get('temp', 'N/A')}°C")
        print(f"   🌬️  Wind: {metar_data[0].get('wspd', 'N/A')} knots from {metar_data[0].get('wdir', 'N/A')}°")
        print(f"   👁️  Visibility: {metar_data[0].get('visib', 'N/A')} statute miles")
        print(f"   ☁️  Sky: {metar_data[0].get('cover', 'N/A')}")
        print(f"   📝 Raw METAR: {metar_data[0].get('rawOb', 'N/A')}")
        print()

        # Save sample data for reference
        with open('data/sample_aviation_weather.json', 'w') as f:
            json.dump(metar_data, f, indent=2)
        print(f"   💾 Sample data saved to: data/sample_aviation_weather.json")
    else:
        print(f"   ⚠️  No METAR data available for {AIRPORT_CODE}")
    print()
except Exception as e:
    print(f"   ❌ Error: {e}")
    print()

# Test 3: Aviation Weather API (TAF - Terminal Aerodrome Forecast)
print("3. Testing Aviation Weather API (TAF)...")
aviation_taf_url = f"https://aviationweather.gov/api/data/taf?ids={AIRPORT_CODE}&format=json"

try:
    response = requests.get(aviation_taf_url, timeout=5)
    response.raise_for_status()
    taf_data = response.json()

    if taf_data:
        print(f"   ✅ Status: {response.status_code}")
        print(f"   🛩️  Airport: {taf_data[0].get('icaoId', 'N/A')}")
        print(f"   📅 Issue Time: {taf_data[0].get('issueTime', 'N/A')}")
        print(f"   ⏰ Valid Period: {taf_data[0].get('validTimeFrom', 'N/A')} to {taf_data[0].get('validTimeTo', 'N/A')}")
        print(f"   📝 Raw TAF: {taf_data[0].get('rawTAF', 'N/A')[:100]}...")
        print()
    else:
        print(f"   ⚠️  No TAF data available for {AIRPORT_CODE}")
    print()
except Exception as e:
    print(f"   ❌ Error: {e}")
    print()

# Summary
print("=" * 60)
print("Summary: Hybrid Weather Data Strategy")
print("=" * 60)
print()
print("✅ OpenWeather: General weather (temp, humidity, wind)")
print("✅ Aviation Weather: Aviation-specific (visibility, ceiling, conditions)")
print()
print("💡 Recommendation:")
print("   Use BOTH APIs for comprehensive environmental context:")
print("   - OpenWeather: Fast, simple, general conditions")
print("   - Aviation Weather: Professional aviation data (METAR/TAF)")
print()
print("🎯 For hackathon demo:")
print("   'Our system uses official FAA Aviation Weather data'")
print("   'Combined with real-time weather API for comprehensive analysis'")
print()
