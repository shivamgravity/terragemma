"""
Solar & Naismith Turnaround Calculator for Wilderness Expeditions
100% offline, zero-dependency astronomical calculations based on NOAA Solar Formulas.
"""

import math
from datetime import datetime, date, time, timedelta
from typing import Dict, Any, Tuple


def calculate_solar_times(lat: float, lon: float, target_date: date = None) -> Dict[str, Any]:
    """
    Calculate sunrise, sunset, golden hour, and civil dusk using NOAA solar algorithm.
    Returns times in local solar / estimated local time.
    """
    if target_date is None:
        target_date = date.today()

    day_of_year = target_date.timetuple().tm_yday
    
    # Fractional year in radians
    gamma = 2 * math.pi / 365 * (day_of_year - 1)
    
    # Equation of time in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    
    # Solar declination angle in radians
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
            - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))
    
    lat_rad = math.radians(lat)
    
    def get_hour_angle(zenith_deg: float) -> float:
        zenith_rad = math.radians(zenith_deg)
        cos_ha = (math.cos(zenith_rad) / (math.cos(lat_rad) * math.cos(decl))) - (math.tan(lat_rad) * math.tan(decl))
        # Handle midnight sun or polar night
        if cos_ha > 1.0:
            return 0.0  # Sun never rises
        elif cos_ha < -1.0:
            return 180.0  # Sun never sets
        return math.degrees(math.acos(cos_ha))

    # Official zenith: 90.833 degrees (90 deg 50 min)
    ha_official = get_hour_angle(90.833)
    # Civil twilight zenith: 96.0 degrees
    ha_civil = get_hour_angle(96.0)
    # Golden hour zenith: 84.0 degrees (6 degrees above horizon)
    ha_golden = get_hour_angle(84.0)
    
    # Solar noon in minutes from midnight UTC
    # Approximation of time offset by longitude
    # 4 minutes per degree longitude
    solar_noon_utc_min = 720 - (4 * lon) - eqtime
    
    # Convert minutes to HH:MM format
    def min_to_timestr(total_min: float) -> str:
        total_min = total_min % 1440
        hrs = int(total_min // 60)
        mins = int(total_min % 60)
        return f"{hrs:02d}:{mins:02d}"

    def min_to_minutes_of_day(total_min: float) -> int:
        return int(total_min % 1440)

    # Note: For trail users, relative local solar time or standard timezone
    # gives accurate day length and relative sunset duration.
    # Estimated local solar time offset = lon / 15 hours
    approx_tz_offset_hours = round(lon / 15.0)
    offset_min = approx_tz_offset_hours * 60
    
    sunrise_min = (solar_noon_utc_min - ha_official * 4) + offset_min
    sunset_min = (solar_noon_utc_min + ha_official * 4) + offset_min
    golden_start_min = (solar_noon_utc_min + ha_golden * 4) + offset_min
    civil_dusk_min = (solar_noon_utc_min + ha_civil * 4) + offset_min
    
    daylight_minutes = max(0, int((ha_official * 8)))
    daylight_hours = daylight_minutes / 60.0

    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "sunrise": min_to_timestr(sunrise_min),
        "sunset": min_to_timestr(sunset_min),
        "sunset_minutes": min_to_minutes_of_day(sunset_min),
        "golden_hour_start": min_to_timestr(golden_start_min),
        "civil_dusk": min_to_timestr(civil_dusk_min),
        "daylight_hours": round(daylight_hours, 1),
        "daylight_str": f"{int(daylight_hours)}h {int(daylight_minutes % 60)}m",
        "approx_utc_offset": approx_tz_offset_hours
    }


def calculate_turnaround_plan(
    distance_miles: float,
    elevation_gain_ft: float,
    departure_time_str: str,
    solar_info: Dict[str, Any],
    base_pace_mph: float = 2.5,
    rest_stop_minutes: int = 30,
    safety_buffer_minutes: int = 45
) -> Dict[str, Any]:
    """
    Applies Naismith's Rule with Scarf's equivalence to compute safe turnaround plan.
    Naismith's Rule: 1 hour per 3 miles (or 5 km) + 1 hour per 2000 ft (600 m) elevation gain.
    """
    # 1. Base moving time (hours)
    moving_time_hours = distance_miles / max(0.5, base_pace_mph)
    
    # 2. Naismith elevation penalty: 1 hr per 2000 ft ascent
    elevation_penalty_hours = elevation_gain_ft / 2000.0
    
    # Total trail time in minutes (out and back or loop)
    total_trail_minutes = int((moving_time_hours + elevation_penalty_hours) * 60) + rest_stop_minutes
    
    # Halfway time (for out-and-back or midpoint of loop)
    halfway_minutes = total_trail_minutes // 2
    
    # Parse departure time
    dep_h, dep_m = map(int, departure_time_str.split(":"))
    dep_total_min = dep_h * 60 + dep_m
    
    # Estimated finish time
    finish_total_min = dep_total_min + total_trail_minutes
    
    # Turnaround timestamp
    turnaround_total_min = dep_total_min + halfway_minutes
    
    # Sunset deadline
    sunset_min = solar_info["sunset_minutes"]
    hard_deadline_min = sunset_min - safety_buffer_minutes
    
    # Daylight remaining at finish
    margin_min = sunset_min - finish_total_min
    
    def min_to_hhmm(m: int) -> str:
        m = m % 1440
        return f"{m//60:02d}:{m%60:02d}"

    # Status assessment
    if margin_min >= 60:
        status = "SAFE"
        status_color = "green"
        recommendation = "Optimal daylight window. You will finish with plenty of sunlight to spare."
    elif margin_min >= 15:
        status = "CAUTION"
        status_color = "orange"
        recommendation = "Tight daylight buffer. Carry a charged headlamp and adhere strictly to turnaround time."
    else:
        status = "HAZARDOUS"
        status_color = "red"
        recommendation = "High risk of night hiking. Either depart earlier, shorten the route, or enforce strict early turnaround."

    return {
        "departure_time": departure_time_str,
        "estimated_duration_hours": round(total_trail_minutes / 60.0, 1),
        "estimated_duration_str": f"{total_trail_minutes // 60}h {total_trail_minutes % 60}m",
        "turnaround_time": min_to_hhmm(turnaround_total_min),
        "estimated_finish_time": min_to_hhmm(finish_total_min),
        "sunset_time": solar_info["sunset"],
        "civil_dusk": solar_info["civil_dusk"],
        "daylight_margin_minutes": margin_min,
        "margin_str": f"{margin_min} min" if margin_min >= 0 else f"{abs(margin_min)} min AFTER sunset",
        "status": status,
        "status_color": status_color,
        "recommendation": recommendation,
        "naismith_details": {
            "distance_miles": distance_miles,
            "elevation_gain_ft": elevation_gain_ft,
            "base_pace_mph": base_pace_mph,
            "elevation_penalty_min": int(elevation_penalty_hours * 60),
            "rest_time_min": rest_stop_minutes
        }
    }
