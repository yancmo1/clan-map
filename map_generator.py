import folium
import json
import requests

def geocode(location):
    if location.lower() == "unknown":
        return None, None
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    res = requests.get(url).json()
    if res:
        return float(res[0]['lat']), float(res[0]['lon'])
    return None, None

def generate_map(data_file="clan_data.json", output_file="templates/map.html"):
    with open(data_file) as f:
        members = json.load(f)

    m = folium.Map(location=[20, 0], zoom_start=2)

    for member in members:
        lat, lon = geocode(member["location"])
        if lat and lon:
            folium.Marker([lat, lon], tooltip=member["name"]).add_to(m)

    m.save(output_file)
