# -*- coding: utf-8 -*-
"""
=========================================================================================
SOLAR POWER MONITORING SYSTEM
Advanced Real-Time Solar Photovoltaic Data Acquisition & Analytics Dashboard
=========================================================================================
Style: Professional Industrial / Scientific / High Clarity & Balanced Scale
Standardized Units: Power in W, Energy in kWh everywhere in UI and Exports
Icon System: Unified Lucide-Style SVG (Dependency-Free, Stroke-Based)
Atmosphere: Dynamic Sun Orb & Solar Trajectory Synchronized with Tehran Ephemeris
Backend: Robust Paho MQTT Engine with Singleton Data Cache
=========================================================================================
"""

import streamlit as st
import paho.mqtt
import paho.mqtt.client as mqtt
import pandas as pd
import time
import requests
from datetime import datetime, timedelta
import pytz
import jdatetime
import math
import os

# =========================================================================================
# 1. PAGE CONFIGURATION & METADATA
# =========================================================================================
st.set_page_config(
    page_title="Solar Power Monitoring Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================================
# 2. PROFESSIONAL UNIFIED ICON SYSTEM (LUCIDE SVG SPECIFICATION)
# =========================================================================================
def get_icon(name: str, size: int = 17, color: str = "currentColor", stroke_width: float = 1.8) -> str:
    """Returns a clean, resolution-independent inline SVG icon in refined Lucide style."""
    paths = {
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
        'sun-dim': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m5 5 1.5 1.5"/><path d="m17.5 17.5 1.5 1.5"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m5 19 1.5-1.5"/><path d="m17.5 6.5 1.5-1.5"/>',
        'zap': '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
        'gauge': '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
        'activity': '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
        'thermometer': '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>',
        'battery-charging': '<path d="M15 7h1a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-2"/><path d="M6 7H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h1"/><path d="m11 7-3 5h4l-3 5"/><line x1="22" x2="22" y1="11" y2="13"/>',
        'calendar': '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/>',
        'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        'cloud-sun': '<path d="M12 2v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="M20 12h2"/><path d="m19.07 4.93-1.41 1.41"/><path d="M15.947 12.65a4 4 0 0 0-5.925-4.128"/><path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6z"/>',
        'wifi': '<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" x2="12.01" y1="20" y2="20"/>',
        'shield-check': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
        'database': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
        'refresh': '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
        'layers': '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
        'bell': '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
        'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
        'sunset': '<path d="M12 10V2"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m8 6 4-4 4 4"/><path d="M16 18a4 4 0 0 0-8 0"/>',
        'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        'sliders': '<line x1="4" x2="20" y1="21" y2="21"/><line x1="4" x2="20" y1="14" y2="14"/><line x1="4" x2="20" y1="7" y2="7"/><circle cx="14" cy="21" r="2"/><circle cx="8" cy="14" r="2"/><circle cx="16" cy="7" r="2"/>',
        'trending-up': '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'
    }
    path_markup = paths.get(name, paths['activity'])
    return f'<span class="ui-icon" style="color: {color};"><svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">{path_markup}</svg></span>'

# =========================================================================================
# 3. UNIT CONVERSIONS & ADAPTIVE FORMATTERS
# =========================================================================================
def energy_mwh_to_kwh(val_mwh: float) -> float:
    """Centralized conversion: 1 kWh = 1,000,000 mWh."""
    return val_mwh / 1_000_000.0

def format_energy_kwh(val_kwh: float) -> str:
    """Adaptive precision formatter for kWh values to preserve meaningful resolution."""
    if val_kwh is None or math.isnan(val_kwh):
        return "N/A"
    if val_kwh <= 0:
        return "0.0000"
    elif val_kwh >= 100:
        return f"{val_kwh:.1f}"
    elif val_kwh >= 10:
        return f"{val_kwh:.2f}"
    elif val_kwh >= 1:
        return f"{val_kwh:.3f}"
    elif val_kwh >= 0.01:
        return f"{val_kwh:.4f}"
    else:
        return f"{val_kwh:.5f}"

def format_power_w(val_w: float) -> str:
    """Adaptive precision formatter for electrical power in Watts."""
    if val_w is None or math.isnan(val_w):
        return "0.00"
    if val_w >= 1000:
        return f"{val_w:,.1f}"
    elif val_w >= 10:
        return f"{val_w:.2f}"
    elif val_w >= 1:
        return f"{val_w:.3f}"
    else:
        return f"{val_w:.4f}"

# =========================================================================================
# 4. TEHRAN EPHEMERIS, WEATHER & DYNAMIC SOLAR TRAJECTORY
# =========================================================================================
tehran_tz = pytz.timezone('Asia/Tehran')
now_tehran = datetime.now(tehran_tz)

gregorian_date_str = now_tehran.strftime("%Y-%m-%d")
jalali_obj = jdatetime.date.fromgregorian(date=now_tehran.date())
jalali_date_str = jalali_obj.strftime("%Y/%m/%d")
time_str = now_tehran.strftime("%H:%M:%S")

@st.cache_data(ttl=900)
def get_tehran_weather():
    """Fetches real outdoor ambient temperature for Tehran with offline fallback."""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=35.6892&longitude=51.3890&current=temperature_2m&timezone=Asia%2FTehran"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            temp = res.json().get('current', {}).get('temperature_2m')
            if temp is not None:
                return f"{temp:.1f}°C"
    except Exception:
        pass
    return "18.5°C"

tehran_temp = get_tehran_weather()

def calculate_solar_elevation(lat=35.6892, lon=51.3890, dt=None):
    """Calculates astronomical solar altitude angle for accurate ambient illumination."""
    if dt is None:
        dt = datetime.now(pytz.utc)
    else:
        dt = dt.astimezone(pytz.utc)
    
    day_of_year = dt.timetuple().tm_yday
    hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    declination = 23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 81)))
    time_offset = 4 * lon
    solar_time = hour + (time_offset / 60.0)
    hour_angle = 15 * (solar_time - 12)
    lat_rad = math.radians(lat)
    dec_rad = math.radians(declination)
    ha_rad = math.radians(hour_angle)
    
    sin_elev = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad)
    return math.degrees(math.asin(max(-1.0, min(1.0, sin_elev))))

solar_elev = calculate_solar_elevation(35.6892, 51.3890, now_tehran)

# Dynamic Solar Trajectory & Atmospheric Sun Orb Geometry (Tehran Local Time)
time_in_hours = now_tehran.hour + now_tehran.minute / 60.0 + now_tehran.second / 3600.0
sunrise = 5.75  # ~05:45 Tehran
sunset = 18.50   # ~18:30 Tehran
day_length = sunset - sunrise

if solar_elev > 10.0:
    # Full Daylight Active
    solar_phase = "Daylight Active"
    solar_phase_icon = get_icon('sun', size=17, color='#ea580c')
    bg_gradient = "linear-gradient(145deg, #f8fafc 0%, #edf2f7 50%, #e2e8f0 100%)"
    card_bg = "rgba(255, 255, 255, 0.94)"
    card_border = "rgba(226, 232, 240, 0.95)"
    text_main = "#0f172a"
    text_sub = "#475569"
    text_muted = "#64748b"
    
    # Sun coordinates on natural sky arc
    progress = max(0.0, min(1.0, (time_in_hours - sunrise) / day_length))
    sun_x = 8.0 + (84.0 * progress)  # 8% (left) to 92% (right)
    sun_y = 78.0 - (56.0 * math.sin(math.pi * progress))  # 78% (low) to 22% (midday peak)
    
    if progress < 0.25:
        # Morning Ascent: soft warm tones
        orb_size = 180
        orb_opacity = 0.55
        center_color = "rgba(255, 251, 235, 0.95)"
        mid_color = "rgba(254, 215, 170, 0.55)"
        outer_color = "rgba(251, 146, 60, 0.22)"
        glow_color = "rgba(251, 146, 60, 0.20)"
    elif progress > 0.70:
        # Late Afternoon: warmer amber
        orb_size = 205
        orb_opacity = 0.60
        center_color = "rgba(254, 243, 199, 0.95)"
        mid_color = "rgba(251, 191, 36, 0.55)"
        outer_color = "rgba(245, 158, 11, 0.24)"
        glow_color = "rgba(245, 158, 11, 0.22)"
    else:
        # Peak Midday: brightest radiant center
        orb_size = 220
        orb_opacity = 0.65
        center_color = "rgba(255, 255, 255, 0.98)"
        mid_color = "rgba(254, 240, 138, 0.65)"
        outer_color = "rgba(251, 191, 36, 0.28)"
        glow_color = "rgba(251, 191, 36, 0.24)"

    sun_orb_html = f'''<div class="sun-atmosphere-orb" style="position: fixed; width: {orb_size}px; height: {orb_size}px; border-radius: 50%; background: radial-gradient(circle, {center_color} 0%, {mid_color} 38%, {outer_color} 68%, transparent 85%); box-shadow: 0 0 85px 35px {glow_color}; filter: blur(16px); left: {sun_x:.1f}%; top: {sun_y:.1f}%; transform: translate(-50%, -50%); z-index: 0; pointer-events: none; opacity: {orb_opacity:.2f}; transition: all 1.2s ease-out;"></div>'''

elif solar_elev > -5.0:
    # Twilight / Sunset
    solar_phase = "Twilight / Sunset"
    solar_phase_icon = get_icon('sunset', size=17, color='#f59e0b')
    bg_gradient = "linear-gradient(145deg, #1e1b4b 0%, #312e81 40%, #1e293b 100%)"
    card_bg = "rgba(255, 255, 255, 0.92)"
    card_border = "rgba(226, 232, 240, 0.9)"
    text_main = "#0f172a"
    text_sub = "#475569"
    text_muted = "#64748b"
    
    if time_in_hours > 12.0:
        # Sunset: low toward right horizon, deep peach/amber/orange
        progress = max(0.0, min(1.0, (time_in_hours - 17.5) / 1.5))
        sun_x = 84.0 + (10.0 * progress)
        sun_y = 66.0 + (16.0 * progress)
        orb_size = 230
        orb_opacity = max(0.20, 0.65 - (progress * 0.35))
        center_color = "rgba(254, 215, 170, 0.95)"
        mid_color = "rgba(249, 115, 22, 0.60)"
        outer_color = "rgba(217, 119, 6, 0.25)"
        glow_color = "rgba(234, 88, 12, 0.28)"
    else:
        # Dawn / Early Sunrise: rising from left horizon
        progress = max(0.0, min(1.0, (time_in_hours - 5.0) / 1.0))
        sun_x = 6.0 + (8.0 * progress)
        sun_y = 78.0 - (12.0 * progress)
        orb_size = 190
        orb_opacity = 0.45 + (progress * 0.20)
        center_color = "rgba(254, 215, 170, 0.90)"
        mid_color = "rgba(251, 146, 60, 0.50)"
        outer_color = "rgba(249, 115, 22, 0.20)"
        glow_color = "rgba(251, 146, 60, 0.20)"

    sun_orb_html = f'''<div class="sun-atmosphere-orb" style="position: fixed; width: {orb_size}px; height: {orb_size}px; border-radius: 50%; background: radial-gradient(circle, {center_color} 0%, {mid_color} 38%, {outer_color} 68%, transparent 85%); box-shadow: 0 0 95px 40px {glow_color}; filter: blur(18px); left: {sun_x:.1f}%; top: {sun_y:.1f}%; transform: translate(-50%, -50%); z-index: 0; pointer-events: none; opacity: {orb_opacity:.2f}; transition: all 1.2s ease-out;"></div>'''

else:
    # Night Operational: Sun completely hidden
    solar_phase = "Night Operational"
    solar_phase_icon = get_icon('moon', size=17, color='#6366f1')
    bg_gradient = "linear-gradient(145deg, #090d16 0%, #0f172a 50%, #1e293b 100%)"
    card_bg = "rgba(255, 255, 255, 0.94)"
    card_border = "rgba(226, 232, 240, 0.9)"
    text_main = "#0f172a"
    text_sub = "#475569"
    text_muted = "#64748b"
    sun_orb_html = ""

# =========================================================================================
# 5. INDUSTRIAL / SCIENTIFIC CSS ARCHITECTURE & BALANCED TYPOGRAPHY
# =========================================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #0f172a;
    }}

    .stApp {{
        background: {bg_gradient};
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2.0rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
        max-width: 1680px !important;
        margin: 0 auto !important;
        position: relative !important;
        z-index: 2 !important;
    }}

    .header-bar,
    .dashboard-card,
    div[data-testid="stVerticalBlockBorderWrapper"],
    .hero-power-card,
    .snapshot-card,
    .table-header-pill,
    div[data-testid="stDataFrame"] {{
        position: relative !important;
        z-index: 2 !important;
    }}

    /* Global Icon Wrapper */
    .ui-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        vertical-align: middle;
        line-height: 0;
    }}
    .ui-icon svg {{
        display: block;
    }}

    /* Header Bar */
    .header-bar {{
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 10px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }}
    .header-title-box {{
        display: flex;
        flex-direction: column;
        gap: 2px;
    }}
    .header-main-title {{
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 9px;
        line-height: 1.15;
    }}
    .header-subtitle {{
        font-size: 11.5px;
        font-weight: 400;
        letter-spacing: 0.1px;
        color: #475569;
    }}
    .header-badges {{
        display: flex;
        align-items: center;
        gap: 7px;
        flex-wrap: wrap;
    }}
    .header-pill {{
        background: rgba(248, 250, 252, 0.92);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 20px;
        padding: 4px 11px;
        font-size: 11.5px;
        font-weight: 500;
        color: #334155;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .header-pill-val {{
        font-weight: 600;
        color: #0f172a;
    }}
    .status-dot {{
        width: 7.5px;
        height: 7.5px;
        border-radius: 50%;
        display: inline-block;
    }}
    .status-dot.green {{ background-color: #10b981; box-shadow: 0 0 6px rgba(16, 185, 129, 0.4); }}
    .status-dot.amber {{ background-color: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.4); }}
    .status-dot.red {{ background-color: #ef4444; box-shadow: 0 0 6px rgba(239, 68, 68, 0.4); }}

    /* Cards Base Styling */
    .dashboard-card {{
        background: {card_bg};
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
        margin-bottom: 10px;
    }}
    .card-title {{
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.1px;
        color: #0f172a;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 7px;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(226, 232, 240, 0.75);
    }}

    /* HERO POWER KPI (Standardized in W, 40px Font Size) */
    .hero-power-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 247, 237, 0.9) 100%);
        border: 1px solid rgba(254, 215, 170, 0.9);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 14px rgba(234, 88, 12, 0.045);
        margin-bottom: 10px;
        text-align: left;
    }}
    .hero-title {{
        font-size: 13.5px;
        font-weight: 600;
        letter-spacing: 0.2px;
        color: #c2410c;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
    }}
    .hero-val {{
        font-size: 40px;
        font-weight: 700;
        letter-spacing: -0.8px;
        color: #0f172a;
        line-height: 1.1;
    }}
    .hero-unit {{
        font-size: 17px;
        font-weight: 500;
        color: #ea580c;
        margin-left: 4px;
    }}
    .hero-sub {{
        font-size: 11.5px;
        font-weight: 400;
        color: #64748b;
        margin-top: 4px;
    }}

    /* KPI Grid & Items */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin-bottom: 10px;
    }}
    .kpi-item {{
        background: rgba(248, 250, 252, 0.88);
        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 10px;
        padding: 9px 11px;
        text-align: left;
    }}
    .kpi-item-label {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .kpi-item-val {{
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.15;
    }}
    .kpi-item-unit {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-left: 3px;
    }}

    /* SOLAR PRODUCTION STATUS (Left Column Bottom Section) */
    .prod-status-grid {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    .prod-status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 8px;
        background: rgba(248, 250, 252, 0.88);
        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 8px;
    }}
    .prod-status-label {{
        font-size: 11.5px;
        font-weight: 500;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .prod-status-val {{
        font-size: 13.5px;
        font-weight: 700;
        color: #0f172a;
    }}
    .prod-status-unit {{
        font-size: 11px;
        font-weight: 500;
        color: #d97706;
        margin-left: 2px;
    }}

    /* UNIFIED CHART CONTAINERS (Fixing Overlap & Night Layering) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(16px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035) !important;
        padding: 10px 12px 12px 12px !important;
        margin-bottom: 10px !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        gap: 0.25rem !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVegaLiteChart"],
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stArrowVegaLiteChart"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    div[data-testid="stVegaLiteChart"] summary, div[data-testid="stArrowVegaLiteChart"] summary {{
        display: none !important;
    }}

    .chart-card-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 5px;
        margin-bottom: 4px;
        border-bottom: 1px solid rgba(226, 232, 240, 0.75);
    }}
    .chart-header-title {{
        font-size: 14px;
        font-weight: 600;
        color: #0f172a;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.1px;
    }}

    /* Compact Chart Empty State (Guarantees Consistent Dimensions & Zero Collapse) */
    .chart-empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(248, 250, 252, 0.65);
        border: 1px dashed rgba(203, 213, 225, 0.8);
        border-radius: 8px;
        text-align: center;
        margin-top: 2px;
    }}
    .chart-empty-state.main-empty {{
        height: 270px;
    }}
    .chart-empty-state.sec-empty {{
        height: 165px;
    }}
    .empty-state-title {{
        font-size: 12px;
        font-weight: 600;
        color: #475569;
        margin-top: 6px;
    }}
    .empty-state-sub {{
        font-size: 10.5px;
        color: #94a3b8;
        margin-top: 2px;
    }}

    /* Timeframe Selector Capsule */
    div[data-testid="stRadio"] {{
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 6px;
    }}
    div[role="radiogroup"] {{
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        background: rgba(255, 255, 255, 0.96) !important;
        padding: 4px 10px !important;
        border-radius: 40px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
        gap: 3px;
    }}
    div[role="radiogroup"] label {{
        padding: 3px 9px !important;
        border-radius: 14px !important;
        margin: 0 !important;
    }}
    div[role="radiogroup"] label p {{
        font-size: 11.5px !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }}

    /* Window Span Caption */
    .timeframe-caption-box {{
        display: flex;
        justify-content: center;
        margin-bottom: 7px;
    }}
    .timeframe-caption {{
        font-size: 11.5px;
        color: #475569;
        background: rgba(255, 255, 255, 0.92);
        padding: 3px 12px;
        border-radius: 12px;
        border: 1px solid rgba(226, 232, 240, 0.85);
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.02);
    }}

    /* PERFORMANCE SNAPSHOT 5-COLUMN FULL-WIDTH GRID */
    .snapshot-grid {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 10px;
    }}
    @media (max-width: 1024px) {{
        .snapshot-grid {{
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }}
    }}
    @media (max-width: 640px) {{
        .snapshot-grid {{
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }}
    }}
    .snapshot-card {{
        background: rgba(248, 250, 252, 0.88);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 10px;
        padding: 12px 14px;
        text-align: left;
    }}
    .snapshot-label {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .snapshot-val {{
        font-size: 17px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }}
    .snapshot-unit {{
        font-size: 11.5px;
        font-weight: 500;
        color: #d97706;
        margin-left: 2px;
    }}

    /* SYSTEM STATUS ROWS: COMPACT ROWS WITH 11.5px TYPOGRAPHY */
    .status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        border-bottom: 1px solid #f8fafc;
        font-size: 11.5px;
    }}
    .status-row:last-child {{ border-bottom: none; }}
    .status-label {{
        color: #475569;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .status-val {{
        font-weight: 600;
        color: #0f172a;
    }}
    .status-badge-inline {{
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 10.5px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }}
    .status-green {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
    .status-amber {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
    .status-red {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}

    /* Table Typography & Header Pill */
    .table-header-pill {{
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(14px);
        border-radius: 8px;
        padding: 6px 14px;
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-size: 14px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 8px;
    }}
    div[data-testid="stDataFrame"] * {{
        font-size: 11px !important;
    }}

    /* Sidebar Refinements */
    div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] p {{
        font-size: 12px !important;
    }}
    div[data-testid="stSidebar"] h3 {{
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    /* Download Button */
    div[data-testid="stDownloadButton"] button {{
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        border: 1px solid #1e293b !important;
        padding: 6px 14px !important;
        font-size: 12px !important;
        transition: background 0.2s ease !important;
        width: 100% !important;
    }}
    div[data-testid="stDownloadButton"] button:hover {{
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }}
</style>
""", unsafe_allow_html=True)

if sun_orb_html:
    st.markdown(sun_orb_html, unsafe_allow_html=True)

# =========================================================================================
# 6. PERSISTENT SINGLETON DATA STORE & LOCAL CSV PERSISTENCE
# =========================================================================================
CSV_BACKUP_FILE = 'solar_backup.csv'

def save_point_to_csv(record_dict):
    """Persists real-time sensor measurements to local CSV."""
    df_new = pd.DataFrame([record_dict])
    if not os.path.exists(CSV_BACKUP_FILE):
        df_new.to_csv(CSV_BACKUP_FILE, index=False)
    else:
        df_new.to_csv(CSV_BACKUP_FILE, mode='a', header=False, index=False)

def load_data_from_csv():
    """Restores historical telemetry with backward-compatible unit conversions."""
    if os.path.exists(CSV_BACKUP_FILE):
        try:
            df = pd.read_csv(CSV_BACKUP_FILE)
            if not df.empty:
                if 'power_W' not in df.columns:
                    if 'power_mW' in df.columns:
                        df['power_W'] = df['power_mW'] / 1000.0
                    else:
                        df['power_W'] = (df['voltage_V'] * df['current_mA']) / 1000.0
                
                if 'energy_kWh' not in df.columns:
                    if 'energy_mWh' in df.columns:
                        df['energy_kWh'] = df['energy_mWh'] / 1_000_000.0
                    elif 'energy_Wh' in df.columns:
                        df['energy_kWh'] = df['energy_Wh'] / 1000.0
                    else:
                        df['energy_kWh'] = 0.0

                if 'energy_mWh' not in df.columns:
                    df['energy_mWh'] = df['energy_kWh'] * 1_000_000.0

                return df.tail(1500).to_dict('records')
        except Exception:
            pass
    return []

# Thread-safe persistent in-memory singleton data cache across all Streamlit reruns
@st.cache_resource
def get_sensor_data():
    initial_records = load_data_from_csv()
    initial_energy_mwh = 0.0
    if initial_records:
        last_rec = initial_records[-1]
        if 'energy_mWh' in last_rec:
            initial_energy_mwh = float(last_rec['energy_mWh'])
        elif 'energy_kWh' in last_rec:
            initial_energy_mwh = float(last_rec['energy_kWh']) * 1_000_000.0

    return {
        'voltage': 0.0,
        'current': 0.0,
        'power': 0.0,            # Internal working unit: mW
        'watts': 0.0,            # Irradiance in W/m²
        'lux': 0.0,
        'temp': 0.0,
        'total_energy_mWh': initial_energy_mwh,
        'last_energy_calc_time': None,
        'last_update_time': None,
        'mqtt_connected': False,
        'logging_active': True,
        'reconnect_count': 0,
        'msg_count': 0,
        'events': [],
        'log_records': initial_records
    }

solar_data = get_sensor_data()

def add_event(level: str, text: str):
    t_now = datetime.now(tehran_tz).strftime("%H:%M:%S")
    solar_data['events'].append({'time': t_now, 'level': level, 'text': text})
    if len(solar_data['events']) > 40:
        solar_data['events'].pop(0)

# =========================================================================================
# 7. SIDEBAR CONTROLS & ARCHITECTURE SETTINGS
# =========================================================================================
with st.sidebar:
    st.markdown(f"### {get_icon('sliders', size=17, color='#0f172a')} Dashboard Controls")
    live_update = st.toggle("Live Telemetry Stream", value=True)
    
    st.markdown("---")
    st.markdown(f"### {get_icon('wifi', size=17, color='#0f172a')} Telemetry Broker")
    broker_ip = st.text_input("MQTT Server Host", value="broker.emqx.io")
    broker_port = st.number_input("Port Number", value=1883, min_value=1, max_value=65535)
    base_topic = st.text_input("Base Topic Tree", value="my_powerplant")
    
    st.markdown("---")
    if st.button("Reset Telemetry Session", use_container_width=True):
        solar_data['voltage'] = 0.0
        solar_data['current'] = 0.0
        solar_data['power'] = 0.0
        solar_data['watts'] = 0.0
        solar_data['lux'] = 0.0
        solar_data['temp'] = 0.0
        solar_data['total_energy_mWh'] = 0.0
        solar_data['last_energy_calc_time'] = None
        solar_data['last_update_time'] = None
        solar_data['log_records'].clear()
        solar_data['msg_count'] = 0
        if os.path.exists(CSV_BACKUP_FILE):
            try:
                os.remove(CSV_BACKUP_FILE)
            except Exception:
                pass
        add_event("info", "Session and data logs reset by operator")
        print("[RESET] Telemetry session reset by operator")
        st.rerun()

# =========================================================================================
# 8. ROBUST MQTT INGESTION ENGINE (INITIALIZED EXACTLY ONCE)
# =========================================================================================
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        solar_data['mqtt_connected'] = True
        sub_filter = f"{base_topic}/#"
        client.subscribe(sub_filter)
        add_event("info", f"Connected to broker. Subscribed to {sub_filter}")
        print(f"MQTT connection successful. Subscribed to {sub_filter}")
    else:
        solar_data['mqtt_connected'] = False
        add_event("error", f"Broker connection failed (Code {rc})")
        print(f"MQTT connection failed with return code {rc}")

def on_disconnect(client, userdata, *args, **kwargs):
    solar_data['mqtt_connected'] = False
    solar_data['reconnect_count'] += 1
    add_event("warning", "MQTT broker disconnected")
    print("MQTT broker disconnected. Reconnect attempted.")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic.lower()
        payload_str = msg.payload.decode('utf-8', errors='ignore').strip('\\x00').strip()
        val = float(payload_str)
        t_now = time.time()
        
        solar_data['msg_count'] += 1
        solar_data['last_update_time'] = t_now
        
        sensor_name = topic.split('/')[-1]

        if sensor_name == 'voltage':
            solar_data['voltage'] = val
        elif sensor_name == 'current':
            solar_data['current'] = val
        elif sensor_name == 'power':
            solar_data['power'] = val # stored in mW
        elif sensor_name == 'watts':
            solar_data['watts'] = val # irradiance in W/m²
        elif sensor_name == 'lux':
            solar_data['lux'] = val
        elif sensor_name in ['temperature', 'temp']:
            solar_data['temp'] = val
            
        # Fallback electrical power computation if sensor payload omitted
        if sensor_name in ['voltage', 'current'] and solar_data['power'] <= 0.0:
            solar_data['power'] = solar_data['voltage'] * solar_data['current']

        # Accurate Riemann-sum Numerical Energy Integration
        if solar_data['last_energy_calc_time'] is not None:
            dt_hours = (t_now - solar_data['last_energy_calc_time']) / 3600.0
            if 0 < dt_hours < 0.05: # Max 3-minute gap
                solar_data['total_energy_mWh'] += solar_data['power'] * dt_hours
        solar_data['last_energy_calc_time'] = t_now

        # Periodic snapshot logging (1 Hz rate-limited)
        dt_tehran = datetime.now(tehran_tz)
        cur_power_w = solar_data['power'] / 1000.0
        cur_energy_kwh = energy_mwh_to_kwh(solar_data['total_energy_mWh'])
        
        record = {
            'timestamp': dt_tehran.isoformat(),
            'time_display': dt_tehran.strftime("%H:%M:%S"),
            'voltage_V': round(solar_data['voltage'], 2),
            'current_mA': round(solar_data['current'], 1),
            'power_W': round(cur_power_w, 4),
            'energy_kWh': cur_energy_kwh,
            'energy_mWh': round(solar_data['total_energy_mWh'], 2),
            'temperature_C': round(solar_data['temp'], 1),
            'illuminance_lux': round(solar_data['lux'], 1),
            'irradiance_W_m2': round(solar_data['watts'], 1)
        }
        
        if not solar_data['log_records'] or (t_now - pd.to_datetime(solar_data['log_records'][-1]['timestamp']).timestamp() >= 1.0):
            solar_data['log_records'].append(record)
            if len(solar_data['log_records']) > 1500:
                solar_data['log_records'].pop(0)
            if solar_data['logging_active']:
                save_point_to_csv(record)

    except Exception as e:
        print(f"MQTT message processing error on {msg.topic}: {e}")

@st.cache_resource
def init_mqtt(broker_host: str, broker_port_num: int, topic_filter: str):
    print("Creating MQTT client...")
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    except Exception:
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        except Exception:
            client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    print(f"Connecting to {broker_host}:{broker_port_num}...")
    try:
        client.connect(broker_host, int(broker_port_num), keepalive=60)
    except Exception as err:
        print(f"MQTT connection to {broker_host} failed: {err}")
        if broker_host != "broker.hivemq.com":
            print("Attempting fallback connection to broker.hivemq.com:1883...")
            try:
                client.connect("broker.hivemq.com", 1883, keepalive=60)
                print("Fallback connection to broker.hivemq.com succeeded")
            except Exception as err2:
                print(f"Fallback connection failed: {err2}")
                add_event("error", f"MQTT connection failed: {err2}")

    client.loop_start()
    return client

mqtt_client = init_mqtt(broker_ip, int(broker_port), base_topic)

# =========================================================================================
# 9. TELEMETRY FRESHNESS & DIAGNOSTICS
# =========================================================================================
if solar_data['last_update_time']:
    sec_since_update = time.time() - solar_data['last_update_time']
    if sec_since_update < 60:
        freshness_label = f"{int(sec_since_update)}s ago"
    elif sec_since_update < 3600:
        freshness_label = f"{int(sec_since_update / 60)}m ago"
    else:
        freshness_label = f"{sec_since_update / 3600:.1f}h ago"
        
    if sec_since_update > 30:
        health_status = "Warning: Data Delayed"
        health_color = "amber"
        system_normal = False
    else:
        health_status = "System Normal"
        health_color = "green"
        system_normal = True
else:
    freshness_label = "Waiting for data..."
    health_status = "Waiting for Telemetry"
    health_color = "amber"
    system_normal = False

mqtt_badge_cls = "status-green" if solar_data['mqtt_connected'] else "status-red"
mqtt_badge_txt = "Connected" if solar_data['mqtt_connected'] else "Disconnected"

# =========================================================================================
# 10. REFINED FORMAL HEADER BAR (PAGE TITLE 28px)
# =========================================================================================
st.markdown(f"""
<div class="header-bar">
    <div class="header-title-box">
        <div class="header-main-title">{get_icon('sun', size=26, color='#ea580c', stroke_width=2.2)} SOLAR POWER MONITORING</div>
        <div class="header-subtitle">Clean Energy · Real-time Data · A Greener Tomorrow</div>
    </div>
    <div class="header-badges">
        <div class="header-pill">{get_icon('calendar', size=16, color='#64748b')} <span class="header-pill-val">{jalali_date_str}</span> <span style="font-size:10.5px; opacity:0.75;">({gregorian_date_str})</span></div>
        <div class="header-pill">{get_icon('clock', size=16, color='#64748b')} <span class="header-pill-val">{time_str}</span></div>
        <div class="header-pill">{get_icon('cloud-sun', size=16, color='#0284c7')} <span class="header-pill-val">{tehran_temp}</span> <span style="font-size:10.5px; opacity:0.75;">Tehran</span></div>
        <div class="header-pill {mqtt_badge_cls}"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {mqtt_badge_txt}</div>
        <div class="header-pill">{get_icon('activity', size=16, color='#64748b')} <span class="header-pill-val">{freshness_label}</span></div>
        <div class="header-pill">{solar_phase_icon} <span class="header-pill-val">{solar_phase}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Convert records to DataFrame for analytical slicing
df_raw = pd.DataFrame(solar_data['log_records'])
df_plot = pd.DataFrame()
current_power_w = solar_data['power'] / 1000.0 if solar_data['power'] > 0 else 0.0

if not df_raw.empty and 'timestamp' in df_raw.columns:
    df_raw['dt'] = pd.to_datetime(df_raw['timestamp'])

# =========================================================================================
# 11. THREE-ZONE RESPONSIVE LAYOUT (LEFT / CENTER / RIGHT)
# =========================================================================================
col_left, col_center, col_right = st.columns([1.05, 2.55, 1.05], gap="medium")

# -----------------------------------------------------------------------------------------
# ZONE 1 (LEFT): HERO POWER (40px), ELECTRICAL KPIs & SOLAR PRODUCTION STATUS
# -----------------------------------------------------------------------------------------
with col_left:
    # 1. Hero KPI: Current Power (40px bold value, dominant visual focus)
    power_hero_val = format_power_w(current_power_w)

    st.markdown(f"""
    <div class="hero-power-card">
        <div class="hero-title">{get_icon('zap', size=18, color='#ea580c', stroke_width=2.0)} CURRENT GENERATED POWER</div>
        <div class="hero-val">{power_hero_val}<span class="hero-unit">W</span></div>
        <div class="hero-sub">Live Photovoltaic Power Output</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Smaller KPI Grid (Standardized Units: V, mA, W/m², Lux, °C, kWh; Values: 22px)
    volt_val = solar_data['voltage']
    curr_val = solar_data['current']
    irr_val = solar_data['watts']
    lux_val = solar_data['lux']
    temp_val = solar_data['temp']
    
    total_energy_kwh = energy_mwh_to_kwh(solar_data['total_energy_mWh'])
    energy_disp_val = format_energy_kwh(total_energy_kwh)

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('gauge', size=14, color='#0284c7')} Voltage</div>
            <div class="kpi-item-val">{volt_val:.2f}<span class="kpi-item-unit">V</span></div>
        </div>
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('activity', size=14, color='#0284c7')} Current</div>
            <div class="kpi-item-val">{curr_val:.1f}<span class="kpi-item-unit">mA</span></div>
        </div>
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('sun', size=14, color='#ea580c')} Irradiance</div>
            <div class="kpi-item-val">{irr_val:.1f}<span class="kpi-item-unit">W/m²</span></div>
        </div>
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('sun-dim', size=14, color='#ea580c')} Illuminance</div>
            <div class="kpi-item-val">{lux_val:,.0f}<span class="kpi-item-unit">Lux</span></div>
        </div>
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('thermometer', size=14, color='#ef4444')} Temperature</div>
            <div class="kpi-item-val">{temp_val:.1f}<span class="kpi-item-unit">°C</span></div>
        </div>
        <div class="kpi-item">
            <div class="kpi-item-label">{get_icon('battery-charging', size=14, color='#10b981')} Total Energy</div>
            <div class="kpi-item-val">{energy_disp_val}<span class="kpi-item-unit">kWh</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Solar Production Status (Prominent, natural spacing)
    if not df_raw.empty and 'dt' in df_raw.columns:
        t_max_all = df_raw['dt'].max()
        today_midnight = t_max_all.replace(hour=0, minute=0, second=0, microsecond=0)
        df_today = df_raw[df_raw['dt'] >= today_midnight]
        peak_today_w = df_today['power_W'].max() if not df_today.empty else current_power_w
        e_today_kwh = (df_today['energy_kWh'].iloc[-1] - df_today['energy_kWh'].iloc[0]) if len(df_today) >= 2 else 0.0
    else:
        peak_today_w = current_power_w
        e_today_kwh = 0.0

    if not solar_data['mqtt_connected'] or solar_data['last_update_time'] is None:
        gen_state_label = "Waiting for Telemetry"
        gen_state_color = "#f59e0b"
    elif current_power_w > 0.02:
        gen_state_label = "Active Generation"
        gen_state_color = "#10b981"
    elif solar_elev <= -5:
        gen_state_label = "Night Idle"
        gen_state_color = "#6366f1"
    else:
        gen_state_label = "Standby / Low Light"
        gen_state_color = "#0284c7"

    st.markdown(f"""
    <div class="dashboard-card" style="margin-bottom: 0px;">
        <div class="card-title">{get_icon('trending-up', size=16, color='#ea580c')} SOLAR PRODUCTION STATUS</div>
        <div class="prod-status-grid">
            <div class="prod-status-row">
                <span class="prod-status-label">{get_icon('zap', size=14, color='#ea580c')} Current Power</span>
                <span class="prod-status-val">{power_hero_val}<span class="prod-status-unit">W</span></span>
            </div>
            <div class="prod-status-row">
                <span class="prod-status-label">{get_icon('activity', size=14, color='#0284c7')} Peak Today</span>
                <span class="prod-status-val">{format_power_w(peak_today_w)}<span class="prod-status-unit">W</span></span>
            </div>
            <div class="prod-status-row">
                <span class="prod-status-label">{get_icon('battery-charging', size=14, color='#10b981')} Energy Today</span>
                <span class="prod-status-val">{format_energy_kwh(e_today_kwh)}<span class="prod-status-unit">kWh</span></span>
            </div>
            <div class="prod-status-row">
                <span class="prod-status-label">{get_icon('shield-check', size=14, color='#0284c7')} Generation State</span>
                <span style="font-size: 11.5px; font-weight: 600; color: {gen_state_color};">● {gen_state_label}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# ZONE 2 (CENTER): TIME FILTER, PRIMARY CHART (280px) & 6 SECONDARY CHARTS (3x2)
# -----------------------------------------------------------------------------------------
with col_center:
    # 1. Timeframe Capsule Selector
    timeframe_labels = ["10 Min", "1 Hour", "Today", "All Time"]
    selected_timeframe = st.radio(
        "Chart Window Span",
        options=timeframe_labels,
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )

    span_caption_text = "Displaying recent telemetry stream"
    if not df_raw.empty and 'dt' in df_raw.columns:
        t_max = df_raw['dt'].max()
        if selected_timeframe == "10 Min":
            cutoff = t_max - timedelta(minutes=10)
            df_plot = df_raw[df_raw['dt'] >= cutoff].copy()
            span_caption_text = f"Window: Last 10 Minutes ({len(df_plot)} points recorded)"
        elif selected_timeframe == "1 Hour":
            cutoff = t_max - timedelta(hours=1)
            df_plot = df_raw[df_raw['dt'] >= cutoff].copy()
            span_caption_text = f"Window: Last 1 Hour ({len(df_plot)} points recorded)"
        elif selected_timeframe == "Today":
            today_start = t_max.replace(hour=0, minute=0, second=0, microsecond=0)
            df_plot = df_raw[df_raw['dt'] >= today_start].copy()
            span_caption_text = f"Window: Today's Accumulation ({len(df_plot)} points recorded)"
        else:
            df_plot = df_raw.copy()
            span_caption_text = f"Window: Full Session History ({len(df_plot)} points recorded)"

    st.markdown(f"""
    <div class="timeframe-caption-box">
        <div class="timeframe-caption">{span_caption_text}</div>
    </div>
    """, unsafe_allow_html=True)

    has_chart_data = not df_plot.empty and len(df_plot) >= 2

    # 2. Main Enclosed Container: Power (W) & Irradiance (W/m²) Trajectory (280px Height)
    with st.container(border=True):
        st.markdown(f"""
        <div class="chart-card-header">
            <span class="chart-header-title">{get_icon('activity', size=17, color='#ea580c')} Power (W) & Irradiance (W/m²) Trajectory</span>
            <span style="font-size: 11px; color: #64748b; font-weight: 500;">Dual-Metric Primary Feed</span>
        </div>
        """, unsafe_allow_html=True)
        
        if has_chart_data:
            main_chart_df = df_plot[['time_display', 'power_W', 'irradiance_W_m2']].copy()
            main_chart_df = main_chart_df.rename(columns={'power_W': 'Power (W)', 'irradiance_W_m2': 'Irradiance (W/m²)'})
            main_chart_df = main_chart_df.set_index('time_display')
            st.line_chart(
                main_chart_df,
                color=["#ea580c", "#d97706"],
                height=280,
                use_container_width=True
            )
        else:
            st.markdown(f"""
            <div class="chart-empty-state main-empty">
                {get_icon('activity', size=28, color='#94a3b8')}
                <div class="empty-state-title">Awaiting Telemetry Packets</div>
                <div class="empty-state-sub">Primary trajectory curve will generate as sensor buffer accumulates</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. Six Secondary Charts Arranged in a 3 Columns × 2 Rows Grid (165px Each)
    # Row 1: Voltage (V), Current (mA), Temperature (°C)
    r1_col1, r1_col2, r1_col3 = st.columns(3, gap="small")

    with r1_col1:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('gauge', size=15, color='#0284c7')} Voltage (V)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'voltage_V']].rename(columns={'voltage_V': 'Voltage (V)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#0284c7"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('gauge', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Voltage</div>
                </div>
                """, unsafe_allow_html=True)

    with r1_col2:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('activity', size=15, color='#06b6d4')} Current (mA)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'current_mA']].rename(columns={'current_mA': 'Current (mA)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#06b6d4"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('activity', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Current</div>
                </div>
                """, unsafe_allow_html=True)

    with r1_col3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('thermometer', size=15, color='#ef4444')} Temperature (°C)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'temperature_C']].rename(columns={'temperature_C': 'Temp (°C)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#ef4444"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('thermometer', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Temp</div>
                </div>
                """, unsafe_allow_html=True)

    # Row 2: Illuminance (Lux), Irradiance (W/m²), Energy (kWh)
    r2_col1, r2_col2, r2_col3 = st.columns(3, gap="small")

    with r2_col1:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('sun-dim', size=15, color='#eab308')} Illuminance (Lux)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'illuminance_lux']].rename(columns={'illuminance_lux': 'Illuminance (Lux)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#eab308"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('sun-dim', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Lux</div>
                </div>
                """, unsafe_allow_html=True)

    with r2_col2:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('sun', size=15, color='#f97316')} Irradiance (W/m²)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'irradiance_W_m2']].rename(columns={'irradiance_W_m2': 'Irradiance (W/m²)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#f97316"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('sun', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Irradiance</div>
                </div>
                """, unsafe_allow_html=True)

    with r2_col3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('battery-charging', size=15, color='#10b981')} Energy (kWh)</span>
            </div>
            """, unsafe_allow_html=True)
            if has_chart_data:
                chart_sub = df_plot[['time_display', 'energy_kWh']].rename(columns={'energy_kWh': 'Energy (kWh)'}).set_index('time_display')
                st.line_chart(chart_sub, color=["#10b981"], height=165, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('battery-charging', size=20, color='#94a3b8')}
                    <div class="empty-state-title">Awaiting Energy</div>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# ZONE 3 (RIGHT): SYSTEM STATUS, SOLAR INTENSITY GAUGE, RECENT EVENTS (FIXED), EXPORT
# -----------------------------------------------------------------------------------------
with col_right:
    # 1. System Status Panel: Compact rows with 11.5px typography
    log_status_cls = "status-green" if solar_data['logging_active'] else "status-amber"
    log_status_txt = "Active" if solar_data['logging_active'] else "Paused"

    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-title">{get_icon('shield-check', size=16, color='#0284c7')} SYSTEM STATUS</div>
        <div class="status-row">
            <span class="status-label">{get_icon('shield-check', size=14, color='#0284c7')} Overall Health</span>
            <span class="status-badge-inline status-{health_color}"><span class="status-dot {health_color}"></span> {health_status}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('wifi', size=14, color='#0284c7')} MQTT Broker</span>
            <span class="status-badge-inline {mqtt_badge_cls}"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {mqtt_badge_txt}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('database', size=14, color='#0284c7')} Data Logging</span>
            <span class="status-badge-inline {log_status_cls}">{log_status_txt}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('clock', size=14, color='#0284c7')} Last Packet</span>
            <span class="status-val">{freshness_label}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('refresh', size=14, color='#0284c7')} Reconnects</span>
            <span class="status-val">{solar_data['reconnect_count']}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('layers', size=14, color='#0284c7')} Total Messages</span>
            <span class="status-val">{solar_data['msg_count']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Solar Radiation Intensity (Enhanced Semi-Circular SVG Gauge with Real Irradiance)
    current_irr = solar_data['watts']
    norm_frac = min(max(current_irr / 1000.0, 0.0), 1.0)
    
    if current_irr < 200.0:
        cond_tier = "Low"
        tier_color = "#0284c7"
    elif current_irr <= 650.0:
        cond_tier = "Moderate"
        tier_color = "#d97706"
    else:
        cond_tier = "Strong"
        tier_color = "#ea580c"

    cx, cy, r = 100, 78, 60
    total_arc_len = math.pi * r # ~188.5
    active_offset = total_arc_len * (1.0 - norm_frac)
    angle = math.pi * (1.0 - norm_frac)
    px = cx + r * math.cos(angle)
    py = cy - r * math.sin(angle)

    gauge_svg = (
        '<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 4px 0;">'
        '<svg viewBox="20 10 160 82" style="width: 100%; max-width: 230px; overflow: visible;">'
        '<defs>'
        '<linearGradient id="solarArcGrad" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#38bdf8" />'
        '<stop offset="35%" stop-color="#fbbf24" />'
        '<stop offset="70%" stop-color="#f97316" />'
        '<stop offset="100%" stop-color="#ea580c" />'
        '</linearGradient>'
        '</defs>'
        f'<path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="#e2e8f0" stroke-width="8.5" stroke-linecap="round" />'
        f'<path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="url(#solarArcGrad)" stroke-width="8.5" stroke-linecap="round" stroke-dasharray="{total_arc_len:.2f}" stroke-dashoffset="{active_offset:.2f}" />'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#0f172a" stroke="#ffffff" stroke-width="2.5" />'
        f'<text x="{cx}" y="{cy - 18}" text-anchor="middle" font-size="21" font-weight="700" fill="#0f172a" letter-spacing="-0.3px">{current_irr:.1f}</text>'
        f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="11.5" font-weight="500" fill="#64748b">W/m²</text>'
        '</svg>'
        '<div style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 230px; margin-top: 2px; padding: 0 4px;">'
        '<span style="font-size: 11px; font-weight: 500; color: #64748b;">0 W/m² (Low)</span>'
        f'<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 11.5px; font-weight: 600; color: {tier_color}; background: rgba(241, 245, 249, 0.95); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(226, 232, 240, 0.9);">● {cond_tier}</span>'
        '<span style="font-size: 11px; font-weight: 500; color: #64748b;">>650 (Strong)</span>'
        '</div>'
        '</div>'
    )

    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-title">{get_icon('sun', size=16, color='#ea580c')} SOLAR INTENSITY GAUGE</div>
        {gauge_svg}
    </div>
    """, unsafe_allow_html=True)

    # 3. System Diagnostic Event Feed (Bug Fixed: Clean single-line markup without 4-space markdown indents)
    def render_event_feed_html(events):
        if not events:
            return '<div style="font-size: 11.5px; color: #64748b; padding: 6px 2px;">No recent events recorded.</div>'
        items = []
        for ev in reversed(events[-4:]):
            lvl = ev.get('level', 'info')
            dot_color = '#10b981' if lvl == 'success' else ('#f59e0b' if lvl == 'warning' else ('#ef4444' if lvl == 'error' else '#0284c7'))
            t = ev.get('time', '')
            txt = ev.get('text', '')
            items.append(
                f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 4.5px 0; border-bottom: 1px solid rgba(226, 232, 240, 0.6); font-size: 11px;">'
                f'<div style="display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">'
                f'<span style="color: {dot_color}; font-size: 12px; line-height: 1;">●</span>'
                f'<span style="color: #1e293b; font-weight: 500;">{txt}</span>'
                f'</div>'
                f'<span style="color: #64748b; font-size: 10.5px; margin-left: 8px; flex-shrink: 0;">{t}</span>'
                f'</div>'
            )
        return "".join(items)

    events_rendered_html = render_event_feed_html(solar_data['events'])

    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-title">{get_icon('bell', size=16, color='#64748b')} RECENT EVENTS</div>
        {events_rendered_html}
    </div>
    """, unsafe_allow_html=True)

    # 4. Session Data Export
    if not df_raw.empty:
        csv_data = df_raw.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Session CSV",
            data=csv_data,
            file_name=f"solar_telemetry_{now_tehran.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# =========================================================================================
# 12. FULL-WIDTH PERFORMANCE SNAPSHOT (5 COMPACT METRICS)
# =========================================================================================
if not df_plot.empty and len(df_plot) > 0:
    p_peak = df_plot['power_W'].max()
    p_avg = df_plot['power_W'].mean()
    p_volt = df_plot['voltage_V'].max()
    p_curr = df_plot['current_mA'].max()
    irr_avg = df_plot['irradiance_W_m2'].mean()
else:
    p_peak = current_power_w
    p_avg = current_power_w
    p_volt = solar_data['voltage']
    p_curr = solar_data['current']
    irr_avg = solar_data['watts']

st.markdown(f"""
<div class="dashboard-card" style="margin-top: 6px; margin-bottom: 12px; padding: 12px 14px;">
    <div class="card-title" style="margin-bottom: 8px; font-size: 15px;">{get_icon('zap', size=16, color='#ea580c')} PERFORMANCE SNAPSHOT</div>
    <div class="snapshot-grid">
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('zap', size=13, color='#ea580c')} Peak Power</div>
            <div class="snapshot-val">{format_power_w(p_peak)}<span class="snapshot-unit">W</span></div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('gauge', size=13, color='#0284c7')} Peak Voltage</div>
            <div class="snapshot-val">{p_volt:.2f}<span class="snapshot-unit">V</span></div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('activity', size=13, color='#06b6d4')} Peak Current</div>
            <div class="snapshot-val">{p_curr:.1f}<span class="snapshot-unit">mA</span></div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('activity', size=13, color='#0284c7')} Avg Power</div>
            <div class="snapshot-val">{format_power_w(p_avg)}<span class="snapshot-unit">W</span></div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('sun', size=13, color='#f59e0b')} Avg Irradiance</div>
            <div class="snapshot-val">{irr_avg:.1f}<span class="snapshot-unit">W/m²</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 13. TELEMETRY AUDIT LOG TABLE (FULL WIDTH BOTTOM)
# =========================================================================================
t_col1, t_col2 = st.columns([3, 1], gap="medium")
with t_col1:
    st.markdown(f"""
    <div class="table-header-pill">
        {get_icon('database', size=16, color='#0284c7')} REAL-TIME INGESTION TELEMETRY LOG
    </div>
    """, unsafe_allow_html=True)

with t_col2:
    row_count = st.selectbox("Show Rows", options=[15, 30, 50, 100], index=0, label_visibility="collapsed")

# Read from live singleton records or fallback CSV
df_table = pd.DataFrame(solar_data['log_records'])
if df_table.empty and os.path.exists(CSV_BACKUP_FILE):
    try:
        df_table = pd.read_csv(CSV_BACKUP_FILE)
    except Exception:
        df_table = pd.DataFrame()

if not df_table.empty:
    if 'energy_kWh' not in df_table.columns:
        if 'energy_mWh' in df_table.columns:
            df_table['energy_kWh'] = df_table['energy_mWh'] / 1_000_000.0
        elif 'energy_Wh' in df_table.columns:
            df_table['energy_kWh'] = df_table['energy_Wh'] / 1000.0
        else:
            df_table['energy_kWh'] = 0.0

    if 'power_W' not in df_table.columns:
        if 'power_mW' in df_table.columns:
            df_table['power_W'] = df_table['power_mW'] / 1000.0
        else:
            df_table['power_W'] = (df_table['voltage_V'] * df_table['current_mA']) / 1000.0
            
    display_cols = [
        'time_display', 'voltage_V', 'current_mA', 'power_W', 
        'energy_kWh', 'temperature_C', 'illuminance_lux', 'irradiance_W_m2'
    ]
    avail_cols = [c for c in display_cols if c in df_table.columns]
    df_display = df_table[avail_cols].tail(row_count).iloc[::-1].copy()
    
    clean_col_names = {
        'time_display': 'Time',
        'voltage_V': 'Voltage (V)',
        'current_mA': 'Current (mA)',
        'power_W': 'Power (W)',
        'energy_kWh': 'Energy (kWh)',
        'temperature_C': 'Temp (°C)',
        'illuminance_lux': 'Illuminance (Lux)',
        'irradiance_W_m2': 'Irradiance (W/m²)'
    }
    df_display = df_display.rename(columns=clean_col_names)
    st.dataframe(df_display, use_container_width=True, height=200)
else:
    st.info("Waiting for incoming telemetry packets to populate table...")

# =========================================================================================
# 14. LIVE UPDATE AUTO-RERUN LOOP
# =========================================================================================
if live_update:
    time.sleep(3.5)
    st.rerun()