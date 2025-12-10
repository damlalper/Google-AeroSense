#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aviation Weather API Test - Simple Version
"""

import requests
import json

AIRPORT_CODE = "KJFK"  # New York JFK Airport

print("=" * 60)
print("Aviation Weather API Test (FAA Official Data)")
print("=" * 60)
print()

# Test Aviation Weather API (METAR)
print("Testing Aviation Weather API (METAR)...")
url = f"https://aviationweather.gov/api/data/metar?ids={AIRPORT_CODE}&format=json"

try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data:
            print("\nSUCCESS! Aviation Weather API is working!")
            print("\nSample Data:")
            print(f"  Airport: {data[0].get('icaoId', 'N/A')}")
            print(f"  Temperature: {data[0].get('temp', 'N/A')} C")
            print(f"  Wind Speed: {data[0].get('wspd', 'N/A')} knots")
            print(f"  Visibility: {data[0].get('visib', 'N/A')} miles")
            print(f"  Raw METAR: {data[0].get('rawOb', 'N/A')}")

            # Save sample
            with open('data/sample_aviation_weather.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("\nSample data saved to: data/sample_aviation_weather.json")
        else:
            print("No data returned")
    else:
        print(f"Error: HTTP {response.status_code}")

except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 60)
print("Next Steps:")
print("  1. NASA dataset indir (manuel)")
print("  2. Docker Desktop yukle")
print("  3. Go yukle")
print("  4. Confluent'ta topic olustur")
print("=" * 60)
