"""
Filename: suburb_research.py
Purpose: Research suburb-to-practice route data for location content blocks
Created: 2026-03-29

Fetches drive time, route roads, and nearby pharmacies for each suburb
using Google Maps Directions API and Places API (New).

Dependencies:
- Google Maps API key in .env (GOOGLE_MAPS_API_KEY)
- Directions API enabled
- Places API (New) enabled

Usage:
  python3 suburb_research.py                    # Process all suburbs
  python3 suburb_research.py Westminster Balga  # Process specific suburbs
"""

import json
import os
import subprocess
import sys
import re

# Load API key from .env
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
API_KEY = None
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith('GOOGLE_MAPS_API_KEY='):
            API_KEY = line.strip().split('=', 1)[1]
            break

if not API_KEY:
    print("ERROR: GOOGLE_MAPS_API_KEY not found in .env")
    sys.exit(1)

# Practice address
PRACTICE_ADDRESS = "3/8 Odin Rd, Innaloo WA 6018, Australia"
PRACTICE_NAME = "Odin House Dental Surgery"

# Suburbs from pages.json (46 unique suburbs across 4 services)
SUBURBS = [
    "Balcatta", "Balga", "Carine", "Churchlands", "City Beach",
    "Coolbinia", "Daglish", "Dianella", "Doubleview", "Duncraig",
    "Floreat", "Girrawheen", "Glendalough", "Greenwood", "Gwelup",
    "Hamersley", "Herdsman", "Innaloo", "Jolimont", "Joondanna",
    "Karrinyup", "Leederville", "Marmion", "Menora", "Mirrabooka",
    "Mount Claremont", "Mount Hawthorn", "Nollamara", "North Beach",
    "North Perth", "Osborne Park", "Scarborough", "Shenton Park",
    "Stirling", "Subiaco", "Trigg", "Tuart Hill", "Warwick",
    "Watermans Bay", "Wembley", "Wembley Downs", "West Leederville",
    "West Perth", "Westminster", "Woodlands", "Yokine"
]

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'suburb_data')


def api_get(url):
    """Fetch URL via curl and return parsed JSON."""
    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True, text=True, timeout=30
    )
    return json.loads(result.stdout)


def get_directions(suburb):
    """Get drive time and route from suburb to practice."""
    origin = f"{suburb} WA Australia"
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin.replace(' ', '+')}"
        f"&destination={PRACTICE_ADDRESS.replace(' ', '+')}"
        f"&key={API_KEY}"
    )
    data = api_get(url)

    if data.get('status') != 'OK' or not data.get('routes'):
        return None

    leg = data['routes'][0]['legs'][0]
    duration = leg['duration']['text']
    distance = leg['distance']['text']

    # Extract main road names from route steps
    roads = []
    for step in leg['steps']:
        html = step.get('html_instructions', '')
        # Pull road names from directions HTML
        road_matches = re.findall(r'<b>(.*?)</b>', html)
        for road in road_matches:
            road_clean = road.strip()
            # Filter out cardinal directions and short tokens
            if road_clean and len(road_clean) > 3 and road_clean not in roads:
                if any(kw in road_clean for kw in ['Rd', 'St', 'Ave', 'Hwy', 'Fwy', 'Dr', 'Way', 'Blvd', 'Cres', 'Pde', 'Tce', 'Road', 'Street', 'Highway', 'Freeway', 'Drive']):
                    roads.append(road_clean)

    # Get midpoint of route for pharmacy search
    overview = data['routes'][0].get('overview_polyline', {}).get('points', '')
    midpoint = None
    if leg.get('steps'):
        mid_idx = len(leg['steps']) // 2
        mid_step = leg['steps'][mid_idx]
        midpoint = mid_step.get('end_location')

    # Determine general direction from practice
    start_lat = leg['start_location']['lat']
    start_lng = leg['start_location']['lng']
    end_lat = leg['end_location']['lat']
    end_lng = leg['end_location']['lng']

    lat_diff = start_lat - end_lat
    lng_diff = start_lng - end_lng

    if abs(lat_diff) > abs(lng_diff):
        direction = "north" if lat_diff > 0 else "south"
    else:
        direction = "east" if lng_diff > 0 else "west"

    # Refine to include secondary direction if close
    if abs(lat_diff) > 0.005 and abs(lng_diff) > 0.005:
        ns = "north" if lat_diff > 0 else "south"
        ew = "east" if lng_diff > 0 else "west"
        direction = f"{ns}-{ew}"

    return {
        "duration": duration,
        "distance": distance,
        "roads": roads,
        "direction": direction,
        "midpoint": midpoint
    }


def find_pharmacy_on_route(midpoint):
    """Find a pharmacy near the route midpoint using Places API (New)."""
    if not midpoint:
        return None

    lat = midpoint['lat']
    lng = midpoint['lng']

    url = (
        f"https://places.googleapis.com/v1/places:searchNearby"
    )

    payload = json.dumps({
        "includedTypes": ["pharmacy"],
        "maxResultCount": 3,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": 1500.0
            }
        }
    })

    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-H", f"X-Goog-Api-Key: {API_KEY}",
            "-H", "X-Goog-FieldMask: places.displayName,places.formattedAddress,places.shortFormattedAddress",
            "-d", payload
        ],
        capture_output=True, text=True, timeout=30
    )

    data = json.loads(result.stdout)
    places = data.get('places', [])

    if not places:
        return None

    place = places[0]
    return {
        "name": place.get('displayName', {}).get('text', ''),
        "address": place.get('shortFormattedAddress', place.get('formattedAddress', ''))
    }


def research_suburb(suburb):
    """Research a single suburb and return structured data."""
    print(f"  Researching {suburb}...")

    directions = get_directions(suburb)
    if not directions:
        print(f"    WARNING: Could not get directions for {suburb}")
        return {"suburb": suburb, "error": "directions_failed"}

    pharmacy = find_pharmacy_on_route(directions.get('midpoint'))

    result = {
        "suburb": suburb,
        "practice": PRACTICE_NAME,
        "practice_address": PRACTICE_ADDRESS,
        "drive_minutes": directions['duration'],
        "drive_distance": directions['distance'],
        "primary_roads": directions['roads'][:3],
        "direction_from_practice": directions['direction'],
        "pharmacy": pharmacy
    }

    print(f"    {directions['duration']} via {', '.join(directions['roads'][:2]) if directions['roads'] else 'unknown route'}")
    if pharmacy:
        print(f"    Pharmacy: {pharmacy['name']} ({pharmacy['address']})")

    return result


def main():
    # Determine which suburbs to process
    if len(sys.argv) > 1:
        suburbs = sys.argv[1:]
    else:
        suburbs = SUBURBS

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Researching {len(suburbs)} suburbs → {PRACTICE_ADDRESS}\n")

    results = []
    for suburb in suburbs:
        result = research_suburb(suburb)
        results.append(result)

    # Save all results
    output_file = os.path.join(OUTPUT_DIR, 'suburb_research.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. Results saved to {output_file}")

    # Summary
    successful = [r for r in results if 'error' not in r]
    failed = [r for r in results if 'error' in r]
    print(f"Successful: {len(successful)} | Failed: {len(failed)}")
    if failed:
        print(f"Failed suburbs: {', '.join(r['suburb'] for r in failed)}")


if __name__ == '__main__':
    main()
