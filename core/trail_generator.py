"""
Trail Expedition Generator & Sensory Landmark Guide
Produces screen-minimizing sensory anchors and interactive open geospatial maps.
"""

import json
from typing import Dict, Any, List
import folium
from core.gemma_engine import gemma


def generate_sensory_field_guide(
    trail_name: str,
    region: str,
    distance_miles: float,
    elevation_gain_ft: float,
    terrain: str,
    turnaround_time: str,
    sunset_time: str,
    model: str = "gemma3:1b"
) -> Dict[str, Any]:
    """
    Prompts Gemma 3 to synthesize an 'Eyes-Up, Screen-Down' sensory field guide.
    """
    prompt = f"""You are a veteran backcountry mountain guide for TerraGemma.
Our goal is to get hikers to PUT THEIR SCREENS AWAY and immerse in nature.

Generate an 'Eyes-Up, Screen-Down' Sensory Field Briefing for:
- Trail: {trail_name} ({region})
- Distance: {distance_miles} miles | Elevation Gain: {elevation_gain_ft} ft
- Terrain: {terrain}
- Hard Turnaround Time: {turnaround_time} (Sunset at {sunset_time})

Format your response in crisp markdown with these exact 4 sections:
1. 👂 SENSORY LANDMARK ANCHORS: Give 3 memorable physical anchors (sound, smell, or visual natural landmark) that tell them where they are without looking at a phone screen.
2. ⏱️ DISCIPLINED TURNAROUND PROTOCOL: Emphasize the strict {turnaround_time} turnaround rule to avoid being stranded in the dark.
3. 🎒 MINIMALIST PACK CHECK: 3 vital non-negotiables for this specific terrain.
4. 🌿 MINDFUL 'TOUCH GRASS' MISSION: One specific observation exercise to connect with the landscape (e.g. examining leaf veins, listening for bird calls, feeling tree bark changes).

Be concise, vivid, and grounded in real wilderness wisdom. Keep it under 250 words."""

    system_prompt = (
        "You are TerraGemma, an offline edge AI wilderness guide. "
        "Your mission is to make the screen the shortest part of the hike. "
        "Deliver punchy, vivid sensory cues so the hiker pockets their device immediately."
    )

    result = gemma.generate(prompt=prompt, system_prompt=system_prompt, model=model, temperature=0.3)
    
    # Generate concise audio script for TTS
    audio_script = (
        f"Trail briefing for {trail_name}. Your hard turnaround time is {turnaround_time}, "
        f"with sunset at {sunset_time}. "
        f"Keep your eyes up and phone in your pocket. Rely on your senses: listen for running water, "
        f"watch the tree canopy thin as you gain elevation, and feel the wind shift on the ridge. "
        f"Stay hydrated, respect your turnaround time, and enjoy the wild."
    )

    return {
        "guide_markdown": result["response"],
        "audio_script": audio_script,
        "source": result["source"],
        "latency_ms": result["latency_ms"],
        "turnaround_time": turnaround_time,
        "sunset_time": sunset_time
    }


def build_trail_map(
    trail_data: Dict[str, Any],
    turnaround_time: str = ""
) -> folium.Map:
    """
    Renders an interactive OpenStreetMap view with custom waypoint markers,
    elevation contours, and turnaround highlight.
    """
    center_lat = trail_data["lat"]
    center_lon = trail_data["lon"]
    waypoints = trail_data.get("waypoints", [])

    # Create base map with OpenStreetMap / CartoDB Positron
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # Waypoint icons and colors mapping
    type_styles = {
        "trailhead": {"color": "green", "icon": "play"},
        "water": {"color": "blue", "icon": "tint"},
        "summit": {"color": "red", "icon": "flag"},
        "viewpoint": {"color": "purple", "icon": "eye-open"},
        "landmark": {"color": "orange", "icon": "star"},
        "bluff": {"color": "darkred", "icon": "cloud"},
        "shelter": {"color": "cadetblue", "icon": "home"},
        "ridge": {"color": "darkblue", "icon": "random"},
        "canyon": {"color": "beige", "icon": "chevron-down"},
        "switchback": {"color": "lightgreen", "icon": "refresh"}
    }

    # Connect waypoints with polyline trail route
    trail_coords = [[wp["lat"], wp["lon"]] for wp in waypoints]
    if len(trail_coords) > 1:
        folium.PolyLine(
            trail_coords,
            color="#2d5a27",
            weight=4,
            opacity=0.85,
            dash_array="5, 10",
            tooltip=f"{trail_data['name']} Trail Path"
        ).add_to(m)

    # Add markers
    for i, wp in enumerate(waypoints):
        w_type = wp.get("type", "landmark")
        style = type_styles.get(w_type, {"color": "blue", "icon": "info-sign"})
        
        popup_html = f"""
        <div style="font-family: sans-serif; width: 220px;">
            <h4 style="margin: 0 0 5px 0; color: #2d5a27;">{wp['name']}</h4>
            <p style="margin: 0 0 5px 0; font-size: 12px; color: #555;"><b>Stop {i+1}:</b> {wp.get('desc', '')}</p>
            <span style="background: #e8f5e9; color: #1b5e20; padding: 2px 6px; border-radius: 4px; font-size: 11px; text-transform: uppercase;">{w_type}</span>
            {f'<div style="margin-top: 5px; color: #b71c1c; font-size: 11px;"><b>Turnaround Point:</b> {turnaround_time}</div>' if w_type in ['summit', 'bluff', 'ridge'] and turnaround_time else ''}
        </div>
        """
        
        folium.Marker(
            location=[wp["lat"], wp["lon"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{i+1}. {wp['name']} ({w_type})",
            icon=folium.Icon(color=style["color"], icon=style["icon"])
        ).add_to(m)

    return m
