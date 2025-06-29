import folium
import requests

def get_role_color(role):
    """Return color based on player role"""
    role_colors = {
        'Leader': 'red',
        'Co-Leader': 'orange', 
        'Elder': 'purple',
        'Member': 'blue',
        '': 'gray'  # Default for empty role
    }
    return role_colors.get(role, 'gray')

def get_role_icon_and_emoji(role):
    """Return icon and emoji based on player role (matching Discord bot)"""
    role_data = {
        'Leader': {'icon': 'star', 'emoji': '👑'},
        'Co-Leader': {'icon': 'fire', 'emoji': '🔥'},
        'Elder': {'icon': 'star-o', 'emoji': '⭐'},
        'Member': {'icon': 'user', 'emoji': '👤'},
        '': {'icon': 'question', 'emoji': '❓'}
    }
    return role_data.get(role, {'icon': 'question', 'emoji': '❓'})

def geocode_location(location):
    """Convert location to coordinates"""
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}&limit=1"
        headers = {'User-Agent': 'clan-map-app'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None

def generate_map(clan_data=None, output_file="templates/map.html"):
    # Use provided clan_data or empty list
    if clan_data is None:
        clan_data = []
    
    # Create map centered on world
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Track locations for statistics
    total_members = len(clan_data)
    located_members = 0
    role_counts = {}
    
    # Add markers for each clan member
    for member in clan_data:
        name = member.get('name', 'Unknown')
        location = member.get('location', 'Unknown')
        role = member.get('role', 'Member')
        favorite_troop = member.get('favorite_troop', '')
        
        # Count roles
        role_counts[role] = role_counts.get(role, 0) + 1
        
        # Skip if no valid location
        if location == 'Unknown' or not location:
            continue
            
        # Get coordinates
        lat = member.get('latitude')
        lon = member.get('longitude')
        
        # Geocode if no coordinates stored
        if lat is None or lon is None:
            lat, lon = geocode_location(location)
            
        if lat is not None and lon is not None:
            located_members += 1
            
            # Get role info
            role_info = get_role_icon_and_emoji(role)
            
            # Create popup content with emoji
            popup_content = f"""
            <div style="font-family: Arial, sans-serif; min-width: 200px;">
                <h4 style="margin: 5px 0; color: {get_role_color(role)};">
                    {role_info['emoji']} {name}
                </h4>
                <p style="margin: 3px 0;"><strong>Role:</strong> {role}</p>
                <p style="margin: 3px 0;"><strong>Location:</strong> {location}</p>
                {f'<p style="margin: 3px 0;"><strong>Favorite Troop:</strong> {favorite_troop}</p>' if favorite_troop else ''}
            </div>
            """
            
            # Add marker with role-based styling
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{role_info['emoji']} {name} ({role})",
                icon=folium.Icon(
                    color=get_role_color(role),
                    icon=role_info['icon'],
                    prefix='fa'
                )
            ).add_to(m)
    
    # Save map
    m.save(output_file)
    
    return m
