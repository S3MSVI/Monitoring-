# -*- coding: utf-8 -*-
"""
=========================================================================================
SOLAR POWER MONITORING SYSTEM
Advanced Real-Time Solar Photovoltaic Data Acquisition & Analytics Dashboard
=========================================================================================
Style: Professional Industrial / Scientific / Dense & Elegant
Standardized Units: Power in W, Energy in kWh everywhere in UI and Exports
Icon System: Coherent Lucide-style SVG (Dependency-Free, Stroke-Based)
=========================================================================================
"""

import streamlit as st
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
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================================
# 2. PROFESSIONAL UNIFIED ICON SYSTEM (LUCIDE SVG SPECIFICATION)
# =========================================================================================
def get_icon(name: str, size: int = 15, color: str = "currentColor", stroke_width: float = 1.8) -> str:
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
    """Adaptive precision formatter for kWh values to avoid hiding useful resolution."""
    if val_kwh <= 0:
        return "0.0000"
    elif val_kwh >= 100:
        return f"{val_kwh:.1f}"
    elif val_kwh >= 10:
        return f"{val_kwh:.2f}"
    elif val_kwh >= 1:
        return f"{val_kwh:.3f}"
    elif val_kwh >= 0.001:
        return f"{val_kwh:.4f}"
    else:
        return f"{val_kwh:.6f}"

def format_power_w(val_w: float) -> str:
    """Adaptive precision formatter for power in Watts."""
    if val_w <= 0:
        return "0.00"
    elif val_w >= 100:
        return f"{val_w:.1f}"
    elif val_w >= 10:
        return f"{val_w:.2f}"
    else:
        return f"{val_w:.3f}"

# =========================================================================================
# 4. TIMEZONE & SOLAR CALCULATIONS (TEHRAN)
# =========================================================================================
tehran_tz = pytz.timezone('Asia/Tehran')
now_tehran = datetime.now(tehran_tz)
gregorian_date_str = now_tehran.strftime("%Y-%m-%d")
time_str = now_tehran.strftime("%H:%M:%S")

try:
    j_date = jdatetime.datetime.fromgregorian(datetime=now_tehran)
    jalali_date_str = j_date.strftime("%Y/%m/%d")
except Exception:
    jalali_date_str = gregorian_date_str

# Weather integration via Open-Meteo
@st.cache_data(ttl=300)
def get_tehran_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=35.6892&longitude=51.3890&current=temperature_2m,relative_humidity_2m"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=4)
        if response.status_code == 200:
            data = response.json()
            if 'current' in data:
                temp = data['current'].get('temperature_2m', 'N/A')
                hum = data['current'].get('relative_humidity_2m', 'N/A')
                return f"{temp} °C", f"{hum} %"
    except Exception:
        pass
    return "Unavailable", "Unavailable"

tehran_temp, tehran_hum = get_tehran_weather()

# Dynamic Solar Position & Daylight Atmosphere (Visual Secondary Overlay)
hour = now_tehran.hour
minute = now_tehran.minute
time_in_hours = hour + minute / 60.0

sunrise = 5.5
sunset = 18.75
day_length = sunset - sunrise

if sunrise <= time_in_hours <= sunset:
    progress = (time_in_hours - sunrise) / day_length
    sun_x = 5 + (90 * progress)
    sun_y = 80 - (50 * math.sin(math.pi * progress))
    
    if progress < 0.20:
        opacity = 0.85 - (progress * 2.0)
        sky_overlay = f"linear-gradient(rgba(15, 23, 42, {opacity*0.4}), rgba(254, 215, 170, {opacity*0.6}))"
        sun_color = "rgba(251, 146, 60, 0.85)"
        solar_phase = "Morning"
        solar_phase_icon = get_icon('sun', size=13, color='#fb923c')
    elif progress > 0.80:
        p_sunset = progress - 0.80
        opacity = 0.30 + (p_sunset * 2.0)
        sky_overlay = f"linear-gradient(rgba(30, 41, 59, {opacity*0.4}), rgba(254, 215, 170, {opacity*0.7}))"
        sun_color = "rgba(249, 115, 22, 0.85)"
        solar_phase = "Sunset"
        solar_phase_icon = get_icon('sunset', size=13, color='#f97316')
    elif progress > 0.55:
        opacity = 0.22
        sky_overlay = f"linear-gradient(rgba(255, 255, 255, {opacity}), rgba(254, 243, 199, {opacity + 0.1}))"
        sun_color = "rgba(252, 211, 77, 0.90)"
        solar_phase = "Afternoon"
        solar_phase_icon = get_icon('sun', size=13, color='#f59e0b')
    else:
        opacity = 0.18
        sky_overlay = f"linear-gradient(rgba(248, 250, 252, {opacity}), rgba(224, 242, 254, {opacity + 0.1}))"
        sun_color = "rgba(254, 240, 138, 0.95)"
        solar_phase = "Daylight"
        solar_phase_icon = get_icon('sun', size=13, color='#eab308')
        
    sun_orb_html = f"""
    <div style="
        position: fixed; width: 150px; height: 150px; border-radius: 50%;
        background: radial-gradient(circle, {sun_color} 0%, rgba(253, 224, 71, 0.35) 40%, transparent 70%);
        box-shadow: 0 0 65px 25px rgba(251, 191, 36, 0.22);
        left: {sun_x:.1f}%; top: {sun_y:.1f}%; transform: translate(-50%, -50%);
        z-index: -1; pointer-events: none;
    "></div>
    """
else:
    sky_overlay = "linear-gradient(rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.92))"
    solar_phase = "Night"
    solar_phase_icon = get_icon('moon', size=13, color='#94a3b8')
    sun_orb_html = ""

# =========================================================================================
# 5. REFINED FORMAL CSS STYLING & COMPACT INFORMATION DENSITY
# =========================================================================================
st.markdown(f"""
<style>
    * {{
        font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif !important;
    }}
    
    .stApp, [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: {sky_overlay}, url('https://images.unsplash.com/photo-1509391365360-2e959784a276?q=85&w=2560&auto=format&fit=crop') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }}

    [data-testid="stAppViewBlockContainer"], .main .block-container {{
        max-width: 1600px !important;
        padding-top: 0.8rem !important;
        padding-bottom: 1.8rem !important;
    }}

    /* Professional Icon System Alignment */
    .ui-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        vertical-align: -0.15em;
        line-height: 0;
    }}
    .ui-icon svg {{
        display: inline-block;
    }}

    /* Status Indicator Dots */
    .status-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
        vertical-align: middle;
    }}
    .status-dot.green {{
        background-color: #10b981;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.20);
    }}
    .status-dot.amber {{
        background-color: #f59e0b;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.20);
    }}
    .status-dot.red {{
        background-color: #ef4444;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.20);
    }}

    /* Header Bar: Refined & Compact */
    .header-bar {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        padding: 11px 18px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }}
    .header-title-box {{ display: flex; flex-direction: column; }}
    .header-main-title {{
        font-size: 21px;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.3px;
        line-height: 1.2;
    }}
    .header-subtitle {{
        font-size: 11px;
        color: #64748b;
        font-weight: 400;
        margin-top: 2px;
        letter-spacing: 0.2px;
    }}

    .header-badges {{
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }}
    .header-pill {{
        background: rgba(241, 245, 249, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 24px;
        padding: 4px 9px;
        font-size: 11.5px;
        font-weight: 500;
        color: #334155;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .header-pill-val {{ font-weight: 600; color: #0f172a; }}
    .header-pill.status-green {{ background: rgba(236, 253, 245, 0.9); border-color: rgba(167, 243, 208, 0.9); color: #047857; }}
    .header-pill.status-red {{ background: rgba(254, 242, 242, 0.9); border-color: rgba(254, 202, 202, 0.9); color: #b91c1c; }}
    .header-pill.status-amber {{ background: rgba(254, 243, 199, 0.9); border-color: rgba(253, 230, 138, 0.9); color: #b45309; }}

    /* Cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(14px);
        border-radius: 14px;
        padding: 14px 16px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
        margin-bottom: 12px;
    }}
    .card-heading {{
        font-size: 11.5px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    .card-heading span {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    /* Hero Power Card */
    .hero-power-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(254, 243, 199, 0.40));
        border: 1.5px solid rgba(245, 158, 11, 0.30);
        border-radius: 14px;
        padding: 16px 15px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.06);
        margin-bottom: 12px;
    }}
    .hero-title {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #b45309;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .hero-val {{
        font-size: 38px;
        font-weight: 700;
        color: #0f172a;
        margin: 4px 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }}
    .hero-unit {{
        font-size: 18px;
        font-weight: 500;
        color: #d97706;
        margin-left: 3px;
    }}
    .hero-sub {{
        font-size: 11px;
        color: #64748b;
        font-weight: 400;
        margin-top: 2px;
    }}

    /* KPI Grid */
    .kpi-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 9px; }}
    .kpi-item {{
        background: rgba(248, 250, 252, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.85);
        border-radius: 10px;
        padding: 9px 11px;
        text-align: left;
    }}
    .kpi-item-title {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .kpi-item-val {{
        font-size: 20px;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.2;
    }}
    .kpi-item-unit {{
        font-size: 10.5px;
        font-weight: 400;
        color: #64748b;
        margin-left: 2px;
    }}

    /* Status Items */
    .status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #f1f5f9;
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
    .status-badge {{
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    /* Solar Conditions Meter */
    .scale-bar {{
        height: 7px;
        border-radius: 6px;
        background: linear-gradient(90deg, #93c5fd 0%, #fde047 50%, #f97316 100%);
        position: relative;
        margin: 12px 0 6px 0;
    }}
    .scale-pointer {{
        position: absolute;
        top: -4px;
        width: 15px;
        height: 15px;
        background: #0f172a;
        border: 2px solid #ffffff;
        border-radius: 50%;
        transform: translateX(-50%);
        box-shadow: 0 1px 5px rgba(0,0,0,0.25);
        transition: left 0.5s ease;
    }}
    .scale-labels {{
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        font-weight: 500;
        color: #64748b;
    }}

    /* Event Log List */
    .event-log-container {{
        max-height: 150px;
        overflow-y: auto;
        padding-right: 4px;
    }}
    .event-entry {{
        font-size: 11px;
        padding: 5px 8px;
        border-radius: 6px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(248, 250, 252, 0.9);
        border-left: 3px solid #cbd5e1;
        gap: 6px;
    }}
    .event-entry.info {{ border-left-color: #3b82f6; }}
    .event-entry.warning {{ border-left-color: #f59e0b; background: rgba(254, 243, 199, 0.35); }}
    .event-entry.error {{ border-left-color: #ef4444; background: rgba(254, 242, 242, 0.35); }}

    /* Clean Timeframe Radio */
    div[data-testid="stRadio"] {{
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 8px;
    }}
    div[role="radiogroup"] {{
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 3px 8px !important;
        border-radius: 40px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
        gap: 2px;
    }}
    div[role="radiogroup"] label {{
        padding: 2px 7px !important;
        border-radius: 14px !important;
        margin: 0 !important;
    }}
    div[role="radiogroup"] label p {{
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }}

    /* Charts */
    div[data-testid="stVegaLiteChart"], div[data-testid="stArrowVegaLiteChart"] {{
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 6px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025) !important;
        border: 1px solid rgba(226, 232, 240, 0.85) !important;
    }}
    div[data-testid="stVegaLiteChart"] summary, div[data-testid="stArrowVegaLiteChart"] summary {{ display: none !important; }}

    h4 {{
        color: #0f172a !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        margin-top: 6px !important;
        margin-bottom: 3px !important;
        letter-spacing: 0.2px;
    }}
    h5 {{
        color: #334155 !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        margin-top: 4px !important;
        margin-bottom: 2px !important;
    }}

    /* Production Summary Section */
    .summary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 10px;
    }}
    .summary-card-item {{
        background: rgba(248, 250, 252, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 10px;
        padding: 9px 12px;
        text-align: left;
    }}
    .summary-item-label {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .summary-item-val {{
        font-size: 17px;
        font-weight: 700;
        color: #0f172a;
    }}
    .summary-item-unit {{
        font-size: 11px;
        font-weight: 500;
        color: #d97706;
        margin-left: 2px;
    }}

    /* Table Typography */
    div[data-testid="stDataFrame"] * {{
        font-size: 11px !important;
    }}

    /* Sidebar Refinements */
    div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] p {{
        font-size: 12px !important;
    }}
    div[data-testid="stSidebar"] h3 {{
        font-size: 13px !important;
        font-weight: 600 !important;
    }}

    /* Download Button */
    div[data-testid="stDownloadButton"] button {{
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 7px !important;
        font-weight: 500 !important;
        border: 1px solid #1e293b !important;
        padding: 5px 12px !important;
        font-size: 11.5px !important;
        transition: background 0.2s ease !important;
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
# 6. BACKEND STORAGE & DATA PERSISTENCE (SOLAR DATA REPOSITORY)
# =========================================================================================
PERSISTENCE_FILE = "solar_backup.csv"

@st.cache_resource
def get_solar_data():
    store = {
        'voltage': 0.0,
        'current': 0.0,
        'power': 0.0,  # in mW
        'temp': 0.0,
        'lux': 0.0,
        'watts': 0.0,
        'total_energy_mWh': 0.0,
        'last_power_time': 0.0,
        'last_msg_time': 0.0,
        'mqtt_connected': False,
        'reconnect_count': 0,
        'msg_count': 0,
        'last_topic': '-',
        'last_payload': '-',
        'logging_active': True,
        'events': [],
        'log_records': []
    }
    
    # Startup restoration from solar_backup.csv
    if os.path.exists(PERSISTENCE_FILE):
        try:
            df = pd.read_csv(PERSISTENCE_FILE)
            if not df.empty:
                records = df.tail(20000).to_dict('records')
                store['log_records'] = records
                last_rec = records[-1]
                
                # Restore last sensor values
                store['voltage'] = float(last_rec.get('voltage_V', last_rec.get('Voltage (V)', 0.0)))
                store['current'] = float(last_rec.get('current_mA', last_rec.get('Current (mA)', 0.0)))
                
                # Restore power: support power_W or legacy power_mW
                if 'power_W' in last_rec:
                    store['power'] = float(last_rec['power_W']) * 1000.0
                else:
                    store['power'] = float(last_rec.get('power_mW', last_rec.get('Power (mW)', 0.0)))
                    
                store['temp'] = float(last_rec.get('temperature_C', last_rec.get('Temp (°C)', 0.0)))
                store['lux'] = float(last_rec.get('illuminance_lux', last_rec.get('Lux', 0.0)))
                store['watts'] = float(last_rec.get('irradiance_W_m2', last_rec.get('Irradiance (W/m²)', 0.0)))
                
                # Restore energy: support energy_kWh, energy_Wh, or energy_mWh
                if 'energy_kWh' in last_rec:
                    store['total_energy_mWh'] = float(last_rec['energy_kWh']) * 1_000_000.0
                elif 'energy_mWh' in last_rec:
                    store['total_energy_mWh'] = float(last_rec['energy_mWh'])
                elif 'energy_Wh' in last_rec:
                    store['total_energy_mWh'] = float(last_rec['energy_Wh']) * 1000.0
                elif 'Energy (mWh)' in last_rec:
                    store['total_energy_mWh'] = float(last_rec['Energy (mWh)'])
                    
                store['events'].append({
                    'time': datetime.now(tehran_tz).strftime("%H:%M:%S"),
                    'text': f"Restored {len(records)} records from {PERSISTENCE_FILE}",
                    'level': 'info'
                })
        except Exception as e:
            store['events'].append({
                'time': datetime.now(tehran_tz).strftime("%H:%M:%S"),
                'text': f"Notice: Could not parse previous archive ({e})",
                'level': 'warning'
            })
            
    return store

solar_data = get_solar_data()

def add_event(msg_text, level="info"):
    now_str = datetime.now(tehran_tz).strftime("%H:%M:%S")
    solar_data['events'].append({'time': now_str, 'text': msg_text, 'level': level})
    if len(solar_data['events']) > 25:
        solar_data['events'].pop(0)

# =========================================================================================
# 7. MQTT PROTOCOL & RELIABILITY CLIENT
# =========================================================================================
def on_connect(client, userdata, flags, rc, properties=None):
    solar_data['mqtt_connected'] = True
    solar_data['reconnect_count'] += 1
    add_event("MQTT Connected to broker successfully", "info")
    client.subscribe("my_powerplant/#")

def on_disconnect(client, userdata, rc, properties=None):
    solar_data['mqtt_connected'] = False
    add_event("MQTT Connection lost (disconnected)", "error")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic.lower()
        payload_str = msg.payload.decode('utf-8', errors='ignore').replace(chr(0), '').strip()
        
        if not payload_str or payload_str.lower() in ['nan', 'null', 'none', 'inf']:
            return
            
        value = float(payload_str)
        if math.isnan(value) or math.isinf(value):
            return
            
        sensor_name = topic.split('/')[-1]
        t_now = time.time()
        solar_data['last_msg_time'] = t_now
        solar_data['msg_count'] += 1
        solar_data['last_topic'] = topic
        solar_data['last_payload'] = payload_str

        # Update sensor values
        if sensor_name == "voltage":
            solar_data['voltage'] = value
        elif sensor_name == "current":
            solar_data['current'] = value
        elif sensor_name == "power":
            solar_data['power'] = value
            # Robust cumulative energy integration (mWh -> Wh -> kWh)
            if solar_data['last_power_time'] > 0:
                delta_h = (t_now - solar_data['last_power_time']) / 3600.0
                if 0 < delta_h < 0.0833 and value > 0:
                    solar_data['total_energy_mWh'] += value * delta_h
            solar_data['last_power_time'] = t_now
        elif sensor_name == "temperature":
            solar_data['temp'] = value
            if value > 55.0:
                add_event(f"High panel temperature alert: {value:.1f} °C", "warning")
        elif sensor_name == "lux":
            solar_data['lux'] = value
        elif sensor_name in ["watts", "irradiance"]:
            solar_data['watts'] = value

        # Record generation (throttled by 1 second)
        current_iso = datetime.now(tehran_tz).isoformat()
        current_hhmmss = datetime.now(tehran_tz).strftime("%H:%M:%S")
        
        last_rec_time = solar_data['log_records'][-1]['time_display'] if solar_data['log_records'] else ""
        if last_rec_time != current_hhmmss:
            power_in_watts = round(solar_data['power'] / 1000.0, 3) if solar_data['power'] > 0 else 0.0
            energy_in_kwh = round(energy_mwh_to_kwh(solar_data['total_energy_mWh']), 7)
            
            record = {
                'timestamp': current_iso,
                'time_display': current_hhmmss,
                'voltage_V': round(solar_data['voltage'], 2),
                'current_mA': round(solar_data['current'], 2),
                'power_W': power_in_watts,
                'energy_kWh': energy_in_kwh,
                'temperature_C': round(solar_data['temp'], 2),
                'illuminance_lux': round(solar_data['lux'], 1),
                'irradiance_W_m2': round(solar_data['watts'], 2)
            }
            solar_data['log_records'].append(record)

            # Auto-backup append to disk
            try:
                df_row = pd.DataFrame([record])
                df_row.to_csv(PERSISTENCE_FILE, mode='a', header=not os.path.exists(PERSISTENCE_FILE), index=False)
                solar_data['logging_active'] = True
            except Exception:
                solar_data['logging_active'] = False

            # Memory ring-buffer bounding
            if len(solar_data['log_records']) > 20000:
                solar_data['log_records'].pop(0)

    except Exception:
        pass

@st.cache_resource
def init_mqtt():
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

    try:
        client.connect("broker.emqx.io", 1883, keepalive=60)
    except Exception:
        try:
            client.connect("broker.hivemq.com", 1883, keepalive=60)
        except Exception as e:
            add_event(f"MQTT init connect error: {e}", "error")

    client.loop_start()
    return client

try:
    mqtt_client = init_mqtt()
except Exception as e:
    st.error(f"MQTT Service Startup Error: {e}")

# =========================================================================================
# 8. SIDEBAR CONTROLS & DATA MANAGEMENT
# =========================================================================================
st.sidebar.markdown(f"### {get_icon('sliders', size=14, color='#64748b')} Controls", unsafe_allow_html=True)
live_update = st.sidebar.checkbox("Live Update", value=True, help="Toggle periodic page refresh for live data streaming.")

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {get_icon('database', size=14, color='#64748b')} Data Management", unsafe_allow_html=True)
confirm_reset = st.sidebar.checkbox("Confirm data reset", value=False, help="Must check before clearing data.")
if st.sidebar.button("Clear All Data & Restart", disabled=not confirm_reset):
    if os.path.exists(PERSISTENCE_FILE):
        try: os.remove(PERSISTENCE_FILE)
        except Exception: pass
    solar_data['log_records'] = []
    solar_data['total_energy_mWh'] = 0.0
    solar_data['last_power_time'] = 0.0
    solar_data['voltage'] = 0.0
    solar_data['current'] = 0.0
    solar_data['power'] = 0.0
    solar_data['temp'] = 0.0
    solar_data['lux'] = 0.0
    solar_data['watts'] = 0.0
    add_event("All persistent and session data cleared by operator", "warning")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "**Solar Power Monitoring System**\n\n"
    "Photovoltaic Data Acquisition\n\n"
    "• Standardized Units: W & kWh\n"
    "• Protocol: MQTT on Wi-Fi\n"
    "• Broker: broker.emqx.io\n"
    "• Timezone: Asia/Tehran"
)

# =========================================================================================
# 9. FRESHNESS & SYSTEM STATUS COMPUTATION
# =========================================================================================
now_epoch = time.time()
if solar_data['last_msg_time'] > 0:
    sec_since_update = now_epoch - solar_data['last_msg_time']
    if sec_since_update < 60:
        freshness_label = f"{sec_since_update:.1f}s ago"
    elif sec_since_update < 3600:
        freshness_label = f"{int(sec_since_update // 60)}m {int(sec_since_update % 60)}s ago"
    else:
        freshness_label = f"{sec_since_update / 3600:.1f}h ago"
        
    if sec_since_update > 30:
        health_status = "Warning: Data Delayed"
        health_color = "status-amber"
        system_normal = False
    else:
        health_status = "System Normal"
        health_color = "status-green"
        system_normal = True
else:
    freshness_label = "Waiting for data..."
    health_status = "Waiting for Telemetry"
    health_color = "status-amber"
    system_normal = False

mqtt_badge_cls = "status-green" if solar_data['mqtt_connected'] else "status-red"
mqtt_badge_txt = "Connected" if solar_data['mqtt_connected'] else "Disconnected"

# =========================================================================================
# 10. REFINED FORMAL HEADER BAR
# =========================================================================================
st.markdown(f"""
<div class="header-bar">
    <div class="header-title-box">
        <div class="header-main-title">{get_icon('sun', size=20, color='#ea580c', stroke_width=2.0)} SOLAR POWER MONITORING</div>
        <div class="header-subtitle">Clean Energy · Real-time Data · A Greener Tomorrow</div>
    </div>
    <div class="header-badges">
        <div class="header-pill">{get_icon('calendar', size=13, color='#64748b')} <span class="header-pill-val">{jalali_date_str}</span> <span style="font-size:10px; opacity:0.75;">({gregorian_date_str})</span></div>
        <div class="header-pill">{get_icon('clock', size=13, color='#64748b')} <span class="header-pill-val">{time_str}</span></div>
        <div class="header-pill">{get_icon('cloud-sun', size=13, color='#0284c7')} <span class="header-pill-val">{tehran_temp}</span> <span style="font-size:10px; opacity:0.75;">Tehran</span></div>
        <div class="header-pill {mqtt_badge_cls}"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {mqtt_badge_txt}</div>
        <div class="header-pill">{get_icon('activity', size=13, color='#64748b')} <span class="header-pill-val">{freshness_label}</span></div>
        <div class="header-pill">{solar_phase_icon} <span class="header-pill-val">{solar_phase}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 11. THREE-ZONE RESPONSIVE LAYOUT
# =========================================================================================
col_left, col_center, col_right = st.columns([1.1, 2.3, 1.2], gap="medium")

# -----------------------------------------------------------------------------------------
# ZONE 1 (LEFT): MAIN KPI & SYSTEM METRICS
# -----------------------------------------------------------------------------------------
with col_left:
    # 1. Hero KPI: Current Power (Standardized to W Everywhere)
    current_power_w = solar_data['power'] / 1000.0 if solar_data['power'] > 0 else 0.0
    power_hero_val = format_power_w(current_power_w)

    st.markdown(f"""
    <div class="hero-power-card">
        <div class="hero-title">{get_icon('zap', size=13, color='#ea580c', stroke_width=2.0)} CURRENT GENERATED POWER</div>
        <div class="hero-val">{power_hero_val}<span class="hero-unit">W</span></div>
        <div class="hero-sub">Live Photovoltaic Power Output</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Smaller KPI Grid (Standardized Units: V, mA, W/m², Lux, °C, kWh)
    volt_val = solar_data['voltage']
    curr_val = solar_data['current']
    irr_val = solar_data['watts']
    lux_val = solar_data['lux']
    temp_val = solar_data['temp']
    
    total_energy_kwh = energy_mwh_to_kwh(solar_data['total_energy_mWh'])
    energy_disp_val = format_energy_kwh(total_energy_kwh)

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>ELECTRICAL & AMBIENT KPIS</span>
        </div>
        <div class="kpi-grid">
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('gauge', size=13, color='#2563eb')} Voltage</div>
                <div class="kpi-item-val">{volt_val:.2f} <span class="kpi-item-unit">V</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('activity', size=13, color='#d97706')} Current</div>
                <div class="kpi-item-val">{curr_val:.1f} <span class="kpi-item-unit">mA</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('sun', size=13, color='#f59e0b')} Irradiance</div>
                <div class="kpi-item-val">{irr_val:.1f} <span class="kpi-item-unit">W/m²</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('sun-dim', size=13, color='#eab308')} Illuminance</div>
                <div class="kpi-item-val">{lux_val:.1f} <span class="kpi-item-unit">Lux</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('thermometer', size=13, color='#e11d48')} Panel Temp</div>
                <div class="kpi-item-val">{temp_val:.1f} <span class="kpi-item-unit">°C</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('battery-charging', size=13, color='#059669')} Total Energy</div>
                <div class="kpi-item-val">{energy_disp_val} <span class="kpi-item-unit">kWh</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# ZONE 2 (CENTER): MAIN CHARTS & TEMPORAL TRENDS
# -----------------------------------------------------------------------------------------
with col_center:
    # 1. Real Timestamp-Based Temporal Filters
    timeframe = st.radio(
        label="Time Range Filter",
        options=["1 Min", "5 Mins", "15 Mins", "1 Hour", "12 Hours", "All-Time"],
        index=1,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Filter dataset using true datetime stamps
    if solar_data['log_records']:
        df_records = pd.DataFrame(solar_data['log_records'])
        df_records['dt'] = pd.to_datetime(df_records['timestamp'], errors='coerce')
        
        # Ensure energy_kWh column is present and clean
        if 'energy_kWh' not in df_records.columns:
            if 'energy_mWh' in df_records.columns:
                df_records['energy_kWh'] = df_records['energy_mWh'] / 1_000_000.0
            elif 'energy_Wh' in df_records.columns:
                df_records['energy_kWh'] = df_records['energy_Wh'] / 1000.0
            else:
                df_records['energy_kWh'] = 0.0

        now_dt = datetime.now(tehran_tz)
        if timeframe == "1 Min":
            cutoff = now_dt - timedelta(minutes=1)
        elif timeframe == "5 Mins":
            cutoff = now_dt - timedelta(minutes=5)
        elif timeframe == "15 Mins":
            cutoff = now_dt - timedelta(minutes=15)
        elif timeframe == "1 Hour":
            cutoff = now_dt - timedelta(hours=1)
        elif timeframe == "12 Hours":
            cutoff = now_dt - timedelta(hours=12)
        else:
            cutoff = None

        if cutoff is not None:
            df_chart = df_records[df_records['dt'] >= cutoff]
        else:
            df_chart = df_records

        # Display actual temporal span honestly
        if not df_chart.empty and len(df_chart) > 1:
            span_s = (df_chart['dt'].max() - df_chart['dt'].min()).total_seconds()
            if span_s >= 3600:
                span_str = f"{int(span_s // 3600)}h {int((span_s % 3600) // 60)}m"
            elif span_s >= 60:
                span_str = f"{int(span_s // 60)}m {int(span_s % 60)}s"
            else:
                span_str = f"{int(span_s)}s"
            st.caption(f"Available window: **{span_str}** ({len(df_chart)} records)")
    else:
        df_chart = pd.DataFrame()

    # 2. Main Hero Chart: POWER & IRRADIANCE (Power in W)
    st.markdown("#### Power (W) & Irradiance (W/m²)")
    if not df_chart.empty and len(df_chart) > 0:
        main_plot_df = pd.DataFrame({
            'Time': df_chart['time_display'],
            'Power (W)': df_chart['power_W'],
            'Irradiance (W/m²)': df_chart['irradiance_W_m2']
        }).set_index('Time')
        st.line_chart(main_plot_df, color=["#ea580c", "#f59e0b"], height=210)
    else:
        st.info("Collecting real-time sensor telemetry...")

    # 3. Secondary Compact Charts Grid (High Information Density)
    col_sc1, col_sc2, col_sc3 = st.columns(3)

    with col_sc1:
        st.markdown("##### Voltage (V)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Voltage (V)': df_chart['voltage_V']}).set_index('Time'), color="#2563eb", height=130)
        st.markdown("##### Illuminance (Lux)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Lux': df_chart['illuminance_lux']}).set_index('Time'), color="#ca8a04", height=130)

    with col_sc2:
        st.markdown("##### Current (mA)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Current (mA)': df_chart['current_mA']}).set_index('Time'), color="#d97706", height=130)
        st.markdown("##### Irradiance (W/m²)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Irradiance (W/m²)': df_chart['irradiance_W_m2']}).set_index('Time'), color="#ea580c", height=130)

    with col_sc3:
        st.markdown("##### Temperature (°C)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Temp (°C)': df_chart['temperature_C']}).set_index('Time'), color="#dc2626", height=130)
        # Energy Chart standardized strictly to kWh
        st.markdown("##### Energy (kWh)")
        if not df_chart.empty:
            st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Energy (kWh)': df_chart['energy_kWh']}).set_index('Time'), color="#10b981", height=130)

# -----------------------------------------------------------------------------------------
# ZONE 3 (RIGHT): SYSTEM STATUS, SOLAR CONDITIONS, EVENTS & EXPORT
# -----------------------------------------------------------------------------------------
with col_right:
    # 1. System Status Panel
    logging_status_str = "Active" if solar_data['logging_active'] else "Error"
    logging_status_color = "#10b981" if solar_data['logging_active'] else "#ef4444"

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('shield-check', size=14, color='#0f172a')} SYSTEM STATUS</span>
        </div>
        <div class="status-row">
            <span class="status-label">Overall Health</span>
            <span class="status-badge" style="color: {'#047857' if system_normal else '#b45309'};"><span class="status-dot {'green' if system_normal else 'amber'}"></span> {health_status}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('wifi', size=13, color='#64748b')} MQTT Connection</span>
            <span class="status-badge" style="color: {'#047857' if solar_data['mqtt_connected'] else '#b91c1c'};"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {'Connected' if solar_data['mqtt_connected'] else 'Disconnected'}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('database', size=13, color='#64748b')} Data Logging</span>
            <span class="status-badge" style="color: {logging_status_color};"><span class="status-dot {'green' if solar_data['logging_active'] else 'red'}"></span> {logging_status_str}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('clock', size=13, color='#64748b')} Last Packet</span>
            <span class="status-badge" style="color: #0f172a;">{freshness_label}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('refresh', size=13, color='#64748b')} Reconnect Count</span>
            <span class="status-badge" style="color: #2563eb;">{solar_data['reconnect_count']}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('layers', size=13, color='#64748b')} Total Messages</span>
            <span class="status-badge" style="color: #64748b;">{solar_data['msg_count']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Solar Conditions Panel & Classification
    current_irr = solar_data['watts']
    if current_irr < 200.0:
        cond_label = "Low Solar Intensity"
        pct_pin = min(max(current_irr / 200.0 * 33.0, 5.0), 33.0)
    elif current_irr <= 650.0:
        cond_label = "Moderate Solar Intensity"
        pct_pin = 33.0 + ((current_irr - 200.0) / 450.0 * 34.0)
    else:
        cond_label = "Strong Solar Radiation"
        pct_pin = 67.0 + min(((current_irr - 650.0) / 350.0 * 33.0), 31.0)

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('sun', size=14, color='#ea580c')} SOLAR CONDITIONS</span>
        </div>
        <div style="font-size: 11.5px; color: #475569; margin-bottom: 6px;">
            Solar Intensity: <b style="color: #0f172a;">{cond_label}</b> ({current_irr:.1f} W/m²)
        </div>
        <div class="scale-bar">
            <div class="scale-pointer" style="left: {pct_pin:.1f}%;"></div>
        </div>
        <div class="scale-labels">
            <span>Low (&lt;200)</span>
            <span>Moderate (200–650)</span>
            <span>Strong (&gt;650 W/m²)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Alerts & Recent Events
    event_html_items = ""
    if solar_data['events']:
        for ev in reversed(solar_data['events'][-5:]):
            lvl = ev.get('level', 'info')
            t = ev.get('time', '')
            txt = ev.get('text', '')
            event_html_items += f'<div class="event-entry {lvl}"><span style="color:#0f172a; font-weight:500;">{txt}</span><span style="color:#94a3b8; font-size:10px; margin-left:auto; white-space:nowrap; padding-left:8px;">{t}</span></div>'
    else:
        event_html_items = '<div style="font-size:11px; color:#64748b; padding:3px 0;">No recent events recorded.</div>'

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('bell', size=14, color='#0f172a')} RECENT EVENTS</span>
        </div>
        <div class="event-log-container">
            {event_html_items}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Data Export Action (Standardized to W and kWh)
    if solar_data['log_records']:
        df_export = pd.DataFrame(solar_data['log_records'])
        export_cols = ['timestamp', 'voltage_V', 'current_mA', 'power_W', 'energy_kWh', 'temperature_C', 'illuminance_lux', 'irradiance_W_m2']
        avail_export_cols = [c for c in export_cols if c in df_export.columns]
        csv_export = df_export[avail_export_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV Archive",
            data=csv_export,
            file_name=f"solar_log_{gregorian_date_str}.csv",
            mime="text/csv",
            use_container_width=True
        )

# =========================================================================================
# 12. COMPACT ANALYTICAL "PRODUCTION SUMMARY" SECTION (REAL METRICS ONLY)
# =========================================================================================
if not df_chart.empty and len(df_chart) > 0:
    peak_p_val = df_chart['power_W'].max()
    avg_p_val = df_chart['power_W'].mean()
    avg_irr_val = df_chart['irradiance_W_m2'].mean()
    pts_count = len(df_chart)
    
    # Calculate genuine energy produced within the selected timeframe
    if len(df_chart) > 1 and 'energy_kWh' in df_chart.columns:
        energy_prod_period = max(df_chart['energy_kWh'].iloc[-1] - df_chart['energy_kWh'].iloc[0], 0.0)
    else:
        energy_prod_period = 0.0
        
    peak_p_str = f"{peak_p_val:.2f} <span class='summary-item-unit'>W</span>"
    avg_p_str = f"{avg_p_val:.2f} <span class='summary-item-unit'>W</span>"
    energy_prod_str = f"{format_energy_kwh(energy_prod_period)} <span class='summary-item-unit'>kWh</span>"
    avg_irr_str = f"{avg_irr_val:.1f} <span class='summary-item-unit'>W/m²</span>"
    pts_str = f"{pts_count:,}"
else:
    peak_p_str = "N/A"
    avg_p_str = "N/A"
    energy_prod_str = "N/A"
    avg_irr_str = "N/A"
    pts_str = "0"

st.markdown(f"""
<div class="glass-card" style="margin-top: 4px; margin-bottom: 12px;">
    <div class="card-heading">
        <span>{get_icon('trending-up', size=14, color='#ea580c')} PRODUCTION SUMMARY ({timeframe.upper()})</span>
    </div>
    <div class="summary-grid">
        <div class="summary-card-item">
            <div class="summary-item-label">{get_icon('zap', size=12, color='#ea580c')} Peak Power</div>
            <div class="summary-item-val">{peak_p_str}</div>
        </div>
        <div class="summary-card-item">
            <div class="summary-item-label">{get_icon('activity', size=12, color='#2563eb')} Average Power</div>
            <div class="summary-item-val">{avg_p_str}</div>
        </div>
        <div class="summary-card-item">
            <div class="summary-item-label">{get_icon('battery-charging', size=12, color='#059669')} Energy Produced ({timeframe})</div>
            <div class="summary-item-val">{energy_prod_str}</div>
        </div>
        <div class="summary-card-item">
            <div class="summary-item-label">{get_icon('sun', size=12, color='#f59e0b')} Average Irradiance</div>
            <div class="summary-item-val">{avg_irr_str}</div>
        </div>
        <div class="summary-card-item">
            <div class="summary-item-label">{get_icon('layers', size=12, color='#64748b')} Data Points</div>
            <div class="summary-item-val">{pts_str}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 13. BOTTOM FULL-WIDTH ZONE: RECENT MEASUREMENTS TABLE (W & kWh STANDARDIZED)
# =========================================================================================
col_tbl_head, col_tbl_ctl = st.columns([3, 1])
with col_tbl_head:
    st.markdown("#### Recent Telemetry Measurements")
with col_tbl_ctl:
    row_count = st.selectbox("Rows to display", options=[5, 10, 20, 50], index=1)

if solar_data['log_records']:
    df_table = pd.DataFrame(solar_data['log_records'])
    
    # Ensure energy_kWh column is present
    if 'energy_kWh' not in df_table.columns:
        if 'energy_mWh' in df_table.columns:
            df_table['energy_kWh'] = df_table['energy_mWh'] / 1_000_000.0
        elif 'energy_Wh' in df_table.columns:
            df_table['energy_kWh'] = df_table['energy_Wh'] / 1000.0
        else:
            df_table['energy_kWh'] = 0.0
            
    display_cols = [
        'time_display', 'voltage_V', 'current_mA', 'power_W', 
        'energy_kWh', 'temperature_C', 'illuminance_lux', 'irradiance_W_m2'
    ]
    avail_cols = [c for c in display_cols if c in df_table.columns]
    df_display = df_table[avail_cols].tail(row_count).iloc[::-1].copy()
    
    # Rename for clean technical readability
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