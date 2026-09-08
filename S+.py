# -*- coding: utf-8 -*-
"""
=========================================================================================
SOLAR POWER MONITORING SYSTEM
Advanced Real-Time Solar Photovoltaic Data Acquisition & Analytics Dashboard
=========================================================================================
Style: Professional Industrial / Scientific / Dense & High Contrast
Standardized Units: Power in W, Energy in kWh everywhere in UI and Exports
Icon System: Unified Lucide-Style SVG (Dependency-Free, Stroke-Based)
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================================
# 2. PROFESSIONAL UNIFIED ICON SYSTEM (LUCIDE SVG SPECIFICATION)
# =========================================================================================
def get_icon(name: str, size: int = 16, color: str = "currentColor", stroke_width: float = 1.8) -> str:
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
    elif val_kwh >= 0.001:
        return f"{val_kwh:.4f}"
    else:
        return f"{val_kwh:.6f}"

def format_power_w(val_w: float) -> str:
    """Adaptive precision formatter for power in Watts."""
    if val_w is None or math.isnan(val_w):
        return "N/A"
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

# Dynamic Solar Position & Daylight Atmosphere (Intentional Background Layer)
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
        solar_phase = "Sunrise"
        solar_phase_icon = get_icon('sun', size=16, color='#fb923c')
    elif progress > 0.80:
        p_sunset = progress - 0.80
        opacity = 0.30 + (p_sunset * 2.0)
        sky_overlay = f"linear-gradient(rgba(30, 41, 59, {opacity*0.4}), rgba(254, 215, 170, {opacity*0.7}))"
        sun_color = "rgba(249, 115, 22, 0.85)"
        solar_phase = "Sunset"
        solar_phase_icon = get_icon('sunset', size=16, color='#f97316')
    elif progress > 0.55:
        opacity = 0.22
        sky_overlay = f"linear-gradient(rgba(255, 255, 255, {opacity}), rgba(254, 243, 199, {opacity + 0.1}))"
        sun_color = "rgba(252, 211, 77, 0.90)"
        solar_phase = "Afternoon"
        solar_phase_icon = get_icon('sun', size=16, color='#f59e0b')
    else:
        opacity = 0.18
        sky_overlay = f"linear-gradient(rgba(248, 250, 252, {opacity}), rgba(224, 242, 254, {opacity + 0.1}))"
        sun_color = "rgba(254, 240, 138, 0.95)"
        solar_phase = "Daylight"
        solar_phase_icon = get_icon('sun', size=16, color='#eab308')
        
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
    sky_overlay = "linear-gradient(rgba(15, 23, 42, 0.82), rgba(30, 41, 59, 0.90))"
    solar_phase = "Night"
    solar_phase_icon = get_icon('moon', size=16, color='#94a3b8')
    sun_orb_html = ""

# =========================================================================================
# 5. REFINED FORMAL CSS STYLING & HIGH INFORMATION DENSITY
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
        padding-bottom: 1.6rem !important;
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

    /* Semantic Status Indicator Dots */
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
    .status-dot.slate {{
        background-color: #94a3b8;
        box-shadow: 0 0 0 2px rgba(148, 163, 184, 0.20);
    }}
    .status-dot.blue {{
        background-color: #0284c7;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.20);
    }}
    .status-dot.orange {{
        background-color: #ea580c;
        box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.20);
    }}

    /* Header Bar: Refined & Compact */
    .header-bar {{
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        padding: 10px 18px;
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        margin-bottom: 10px;
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
        background: rgba(241, 245, 249, 0.88);
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
    .header-pill.status-green {{ background: rgba(236, 253, 245, 0.92); border-color: rgba(167, 243, 208, 0.9); color: #047857; }}
    .header-pill.status-red {{ background: rgba(254, 242, 242, 0.92); border-color: rgba(254, 202, 202, 0.9); color: #b91c1c; }}
    .header-pill.status-amber {{ background: rgba(254, 243, 199, 0.92); border-color: rgba(253, 230, 138, 0.9); color: #b45309; }}

    /* Standard High-Contrast Glass Card Component */
    .glass-card {{
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        padding: 12px 14px;
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        margin-bottom: 10px;
    }}
    .card-heading {{
        font-size: 11.5px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 8px;
        padding-bottom: 4px;
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

    /* Hero Power Card (Largest Visual Focus) */
    .hero-power-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(254, 243, 199, 0.45));
        border: 1.5px solid rgba(245, 158, 11, 0.35);
        border-radius: 14px;
        padding: 14px 14px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.07);
        margin-bottom: 10px;
    }}
    .hero-title {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #b45309;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .hero-val {{
        font-size: 38px;
        font-weight: 700;
        color: #0f172a;
        margin: 2px 0;
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
        margin-top: 1px;
    }}

    /* Electrical & Ambient KPI Grid */
    .kpi-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 7px; }}
    .kpi-item {{
        background: rgba(248, 250, 252, 0.88);
        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 10px;
        padding: 7px 9px;
        text-align: left;
    }}
    .kpi-item-title {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .kpi-item-val {{
        font-size: 18.5px;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.2;
    }}
    .kpi-item-unit {{
        font-size: 10px;
        font-weight: 400;
        color: #64748b;
        margin-left: 2px;
    }}

    /* SOLAR PRODUCTION STATUS (Left Column Bottom Section) */
    .prod-status-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 7px;
    }}
    .prod-status-item {{
        background: rgba(248, 250, 252, 0.88);
        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 10px;
        padding: 7px 9px;
        text-align: left;
    }}
    .prod-status-label {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .prod-status-val {{
        font-size: 17px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
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
        padding: 8px 10px 10px 10px !important;
        margin-bottom: 8px !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        gap: 0.2rem !important;
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
        padding-bottom: 4px;
        margin-bottom: 3px;
        border-bottom: 1px solid rgba(226, 232, 240, 0.75);
    }}
    .chart-header-title {{
        font-size: 12px;
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
        height: 200px;
    }}
    .chart-empty-state.sec-empty {{
        height: 125px;
    }}
    .empty-state-title {{
        font-size: 11.5px;
        font-weight: 600;
        color: #475569;
        margin-top: 5px;
    }}
    .empty-state-sub {{
        font-size: 10px;
        color: #94a3b8;
        margin-top: 1px;
    }}

    /* Timeframe Selector Capsule */
    div[data-testid="stRadio"] {{
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 5px;
    }}
    div[role="radiogroup"] {{
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        background: rgba(255, 255, 255, 0.96) !important;
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

    /* Window Span Caption */
    .timeframe-caption-box {{
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
    }}
    .timeframe-caption {{
        font-size: 11px;
        color: #475569;
        background: rgba(255, 255, 255, 0.92);
        padding: 2px 10px;
        border-radius: 12px;
        border: 1px solid rgba(226, 232, 240, 0.85);
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.02);
    }}

    /* PERFORMANCE SNAPSHOT 5-COLUMN COMPACT GRID */
    .snapshot-grid {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 8px;
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
        padding: 8px 11px;
        text-align: left;
    }}
    .snapshot-label {{
        font-size: 11px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 2px;
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
        font-size: 11px;
        font-weight: 500;
        color: #d97706;
        margin-left: 2px;
    }}

    /* SYSTEM STATUS ROWS: 25% REDUCED VERTICAL SPACING & STRONGER EMPHASIS */
    .status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        border-bottom: 1px solid #f8fafc;
        font-size: 11px;
    }}
    .status-row:last-child {{ border-bottom: none; }}
    .status-label {{
        color: #475569;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
    }}
    .status-badge {{
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 11.5px;
    }}

    /* Event Log List */
    .event-log-container {{
        max-height: 130px;
        overflow-y: auto;
        padding-right: 4px;
    }}
    .event-entry {{
        font-size: 11px;
        padding: 4px 7px;
        border-radius: 6px;
        margin-bottom: 3px;
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

    /* Table Typography & Header Pill */
    .table-header-pill {{
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(14px);
        border-radius: 8px;
        padding: 5px 12px;
        border: 1px solid rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 6px;
    }}
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
# 6. SESSION STATE & LOCAL CSV LOG PERSISTENCE (STANDARDIZED W & kWh)
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
                # Standardize legacy power column
                if 'power_W' not in df.columns:
                    if 'power_mW' in df.columns:
                        df['power_W'] = df['power_mW'] / 1000.0
                    else:
                        df['power_W'] = (df['voltage_V'] * df['current_mA']) / 1000.0
                
                # Standardize legacy energy column
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

if 'solar_data' not in st.session_state:
    st.session_state.solar_data = {
        'voltage': 0.0,
        'current': 0.0,
        'power': 0.0,           # Internal working unit: mW
        'watts': 0.0,           # Irradiance in W/m²
        'lux': 0.0,
        'temp': 0.0,
        'total_energy_mWh': 0.0, # Internal accumulation: mWh
        'last_energy_calc_time': None,
        'last_update_time': None,
        'mqtt_connected': False,
        'logging_active': True,
        'reconnect_count': 0,
        'msg_count': 0,
        'events': [],
        'log_records': load_data_from_csv()
    }
    
    # Initialize accumulated energy from historical records if present
    if st.session_state.solar_data['log_records']:
        last_rec = st.session_state.solar_data['log_records'][-1]
        if 'energy_mWh' in last_rec:
            st.session_state.solar_data['total_energy_mWh'] = float(last_rec['energy_mWh'])
        elif 'energy_kWh' in last_rec:
            st.session_state.solar_data['total_energy_mWh'] = float(last_rec['energy_kWh']) * 1_000_000.0

solar_data = st.session_state.solar_data

def add_event(level: str, text: str):
    t_now = datetime.now(tehran_tz).strftime("%H:%M:%S")
    solar_data['events'].append({'time': t_now, 'level': level, 'text': text})
    if len(solar_data['events']) > 40:
        solar_data['events'].pop(0)

# =========================================================================================
# 7. SIDEBAR CONTROLS & ARCHITECTURE SETTINGS
# =========================================================================================
with st.sidebar:
    st.markdown(f"### {get_icon('sliders', size=16, color='#0f172a')} Dashboard Controls")
    live_update = st.toggle("Live Telemetry Stream", value=True)
    
    st.markdown("---")
    st.markdown(f"### {get_icon('wifi', size=16, color='#0f172a')} Telemetry Broker")
    broker_ip = st.text_input("MQTT Server Host", value="broker.hivemq.com")
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
        solar_data['log_records'] = []
        solar_data['msg_count'] = 0
        if os.path.exists(CSV_BACKUP_FILE):
            try:
                os.remove(CSV_BACKUP_FILE)
            except Exception:
                pass
        add_event("info", "Session and data logs reset by operator")
        st.rerun()

# =========================================================================================
# 8. MQTT INGESTION ENGINE
# =========================================================================================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        solar_data['mqtt_connected'] = True
        client.subscribe(f"{base_topic}/#")
        add_event("info", "MQTT connection established")
    else:
        solar_data['mqtt_connected'] = False
        add_event("error", f"Broker connection failed (Code {rc})")

def on_disconnect(client, userdata, rc):
    solar_data['mqtt_connected'] = False
    solar_data['reconnect_count'] += 1
    add_event("warning", "MQTT broker disconnected")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload_str = msg.payload.decode('utf-8')
        val = float(payload_str)
        t_now = time.time()
        
        solar_data['msg_count'] += 1
        sub_topic = topic.split('/')[-1]

        if sub_topic == 'voltage':
            solar_data['voltage'] = val
        elif sub_topic == 'current':
            solar_data['current'] = val
        elif sub_topic == 'power':
            solar_data['power'] = val # stored in mW
        elif sub_topic == 'watts':
            solar_data['watts'] = val # irradiance in W/m²
        elif sub_topic == 'lux':
            solar_data['lux'] = val
        elif sub_topic == 'temp':
            solar_data['temp'] = val
            
        # Fallback electrical power computation if sensor payload omitted
        if sub_topic in ['voltage', 'current'] and solar_data['power'] <= 0.0:
            solar_data['power'] = solar_data['voltage'] * solar_data['current']

        # Accurate Riemann-sum Numerical Energy Integration
        if solar_data['last_energy_calc_time'] is not None:
            dt_hours = (t_now - solar_data['last_energy_calc_time']) / 3600.0
            if 0 < dt_hours < 0.05: # Max 3-minute gap
                solar_data['total_energy_mWh'] += solar_data['power'] * dt_hours
        solar_data['last_energy_calc_time'] = t_now
        solar_data['last_update_time'] = t_now

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

    except Exception:
        pass

@st.cache_resource
def get_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    return client

mqtt_client = get_mqtt_client()
if not solar_data['mqtt_connected']:
    try:
        mqtt_client.connect_async(broker_ip, int(broker_port), 60)
        mqtt_client.loop_start()
    except Exception:
        pass

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
# 10. REFINED FORMAL HEADER BAR
# =========================================================================================
st.markdown(f"""
<div class="header-bar">
    <div class="header-title-box">
        <div class="header-main-title">{get_icon('sun', size=22, color='#ea580c', stroke_width=2.0)} SOLAR POWER MONITORING</div>
        <div class="header-subtitle">Clean Energy · Real-time Data · A Greener Tomorrow</div>
    </div>
    <div class="header-badges">
        <div class="header-pill">{get_icon('calendar', size=16, color='#64748b')} <span class="header-pill-val">{jalali_date_str}</span> <span style="font-size:10px; opacity:0.75;">({gregorian_date_str})</span></div>
        <div class="header-pill">{get_icon('clock', size=16, color='#64748b')} <span class="header-pill-val">{time_str}</span></div>
        <div class="header-pill">{get_icon('cloud-sun', size=16, color='#0284c7')} <span class="header-pill-val">{tehran_temp}</span> <span style="font-size:10px; opacity:0.75;">Tehran</span></div>
        <div class="header-pill {mqtt_badge_cls}"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {mqtt_badge_txt}</div>
        <div class="header-pill">{get_icon('activity', size=16, color='#64748b')} <span class="header-pill-val">{freshness_label}</span></div>
        <div class="header-pill">{solar_phase_icon} <span class="header-pill-val">{solar_phase}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 11. THREE-ZONE RESPONSIVE LAYOUT
# =========================================================================================
col_left, col_center, col_right = st.columns([1.1, 2.3, 1.2], gap="medium")

# -----------------------------------------------------------------------------------------
# ZONE 1 (LEFT): HERO KPI, ELECTRICAL/AMBIENT KPIS & SOLAR PRODUCTION STATUS
# -----------------------------------------------------------------------------------------
with col_left:
    # 1. Hero KPI: Current Power (Standardized to W Everywhere, Dominant Visual Focus)
    current_power_w = solar_data['power'] / 1000.0 if solar_data['power'] > 0 else 0.0
    power_hero_val = format_power_w(current_power_w)

    st.markdown(f"""
    <div class="hero-power-card">
        <div class="hero-title">{get_icon('zap', size=18, color='#ea580c', stroke_width=2.0)} CURRENT GENERATED POWER</div>
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
                <div class="kpi-item-title">{get_icon('gauge', size=16, color='#2563eb')} Voltage</div>
                <div class="kpi-item-val">{volt_val:.2f} <span class="kpi-item-unit">V</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('activity', size=16, color='#d97706')} Current</div>
                <div class="kpi-item-val">{curr_val:.1f} <span class="kpi-item-unit">mA</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('sun', size=16, color='#f59e0b')} Irradiance</div>
                <div class="kpi-item-val">{irr_val:.1f} <span class="kpi-item-unit">W/m²</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('sun-dim', size=16, color='#ca8a04')} Illuminance</div>
                <div class="kpi-item-val">{lux_val:.1f} <span class="kpi-item-unit">Lux</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('thermometer', size=16, color='#e11d48')} Panel Temp</div>
                <div class="kpi-item-val">{temp_val:.1f} <span class="kpi-item-unit">°C</span></div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-title">{get_icon('battery-charging', size=16, color='#059669')} Total Energy</div>
                <div class="kpi-item-val">{energy_disp_val} <span class="kpi-item-unit">kWh</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Dedicated Section: SOLAR PRODUCTION STATUS (Derived from genuine real-time data)
    today_date_str = now_tehran.strftime("%Y-%m-%d")
    today_records = [r for r in solar_data['log_records'] if r.get('timestamp', '').startswith(today_date_str)]
    
    if today_records:
        power_vals_today = [r.get('power_W', 0.0) for r in today_records if r.get('power_W') is not None]
        peak_today_val = max(power_vals_today) if power_vals_today else current_power_w
        if len(today_records) > 1 and 'energy_kWh' in today_records[-1] and 'energy_kWh' in today_records[0]:
            energy_today_val = max(today_records[-1]['energy_kWh'] - today_records[0]['energy_kWh'], 0.0)
        else:
            energy_today_val = total_energy_kwh
    else:
        peak_today_val = current_power_w if current_power_w > 0 else None
        energy_today_val = total_energy_kwh if total_energy_kwh > 0 else 0.0

    cur_prod_str = f"{format_power_w(current_power_w)} <span class='prod-status-unit'>W</span>"
    peak_today_str = f"{format_power_w(peak_today_val)} <span class='prod-status-unit'>W</span>" if peak_today_val is not None else "N/A"
    energy_today_str = f"{format_energy_kwh(energy_today_val)} <span class='prod-status-unit'>kWh</span>"

    # Determine real physical state based on connectivity, freshness, power, and irradiance
    sec_since_up = (time.time() - solar_data['last_update_time']) if solar_data['last_update_time'] else 9999
    if not solar_data['mqtt_connected']:
        prod_state_txt = "Waiting for Telemetry"
        prod_state_dot = "amber"
        prod_state_col = "#b45309"
    elif sec_since_up > 35:
        prod_state_txt = "Waiting for Telemetry"
        prod_state_dot = "amber"
        prod_state_col = "#b45309"
    else:
        if current_power_w >= 0.20:
            prod_state_txt = "Producing"
            prod_state_dot = "green"
            prod_state_col = "#047857"
        elif irr_val >= 50.0:
            prod_state_txt = "Low Output"
            prod_state_dot = "amber"
            prod_state_col = "#b45309"
        else:
            prod_state_txt = "No Production"
            prod_state_dot = "slate"
            prod_state_col = "#64748b"

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('activity', size=16, color='#ea580c')} SOLAR PRODUCTION STATUS</span>
            <span style="font-size: 11px; font-weight: 600; color: {prod_state_col}; display: inline-flex; align-items: center; gap: 4px; text-transform: none;">
                <span class="status-dot {prod_state_dot}"></span> {prod_state_txt}
            </span>
        </div>
        <div class="prod-status-grid">
            <div class="prod-status-item">
                <div class="prod-status-label">{get_icon('zap', size=16, color='#ea580c')} Current Output</div>
                <div class="prod-status-val">{cur_prod_str}</div>
            </div>
            <div class="prod-status-item">
                <div class="prod-status-label">{get_icon('trending-up', size=16, color='#2563eb')} Peak Today</div>
                <div class="prod-status-val">{peak_today_str}</div>
            </div>
            <div class="prod-status-item">
                <div class="prod-status-label">{get_icon('battery-charging', size=16, color='#059669')} Energy Today</div>
                <div class="prod-status-val">{energy_today_str}</div>
            </div>
            <div class="prod-status-item">
                <div class="prod-status-label">{get_icon('shield-check', size=16, color='#64748b')} Generation State</div>
                <div class="prod-status-val" style="font-size: 13.5px; font-weight: 600; color: {prod_state_col}; padding-top: 2px;">
                    <span class="status-dot {prod_state_dot}"></span> {prod_state_txt}
                </div>
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
        
        # Ensure standardized energy and power columns exist
        if 'energy_kWh' not in df_records.columns:
            if 'energy_mWh' in df_records.columns:
                df_records['energy_kWh'] = df_records['energy_mWh'] / 1_000_000.0
            elif 'energy_Wh' in df_records.columns:
                df_records['energy_kWh'] = df_records['energy_Wh'] / 1000.0
            else:
                df_records['energy_kWh'] = 0.0

        if 'power_W' not in df_records.columns:
            if 'power_mW' in df_records.columns:
                df_records['power_W'] = df_records['power_mW'] / 1000.0
            else:
                df_records['power_W'] = (df_records['voltage_V'] * df_records['current_mA']) / 1000.0

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
            st.markdown(f"""
            <div class="timeframe-caption-box">
                <span class="timeframe-caption">Active telemetry window: <b>{span_str}</b> ({len(df_chart)} records)</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        df_chart = pd.DataFrame()

    # 2. Main Hero Chart: POWER (W) & IRRADIANCE (W/m²) inside Integrated Card Container
    with st.container(border=True):
        st.markdown(f"""
        <div class="chart-card-header">
            <span class="chart-header-title">{get_icon('sun', size=16, color='#ea580c')} Power (W) & Irradiance (W/m²)</span>
        </div>
        """, unsafe_allow_html=True)
        if not df_chart.empty and len(df_chart) > 0:
            main_plot_df = pd.DataFrame({
                'Time': df_chart['time_display'],
                'Power (W)': df_chart['power_W'],
                'Irradiance (W/m²)': df_chart['irradiance_W_m2']
            }).set_index('Time')
            st.line_chart(main_plot_df, color=["#ea580c", "#f59e0b"], height=200)
        else:
            st.markdown(f"""
            <div class="chart-empty-state main-empty">
                {get_icon('activity', size=22, color='#94a3b8')}
                <div class="empty-state-title">Collecting real-time sensor telemetry...</div>
                <div class="empty-state-sub">Waiting for incoming solar telemetry packets</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. Secondary Compact Charts Grid (Integrated Card Containers, Zero Overlap)
    col_sc1, col_sc2, col_sc3 = st.columns(3)

    with col_sc1:
        # Voltage (V)
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('gauge', size=16, color='#2563eb')} Voltage (V)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Voltage (V)': df_chart['voltage_V']}).set_index('Time'), color="#2563eb", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('gauge', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

        # Illuminance (Lux)
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('sun-dim', size=16, color='#ca8a04')} Illuminance (Lux)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Lux': df_chart['illuminance_lux']}).set_index('Time'), color="#ca8a04", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('sun-dim', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

    with col_sc2:
        # Current (mA)
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('activity', size=16, color='#d97706')} Current (mA)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Current (mA)': df_chart['current_mA']}).set_index('Time'), color="#d97706", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('activity', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

        # Irradiance (W/m²)
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('sun', size=16, color='#ea580c')} Irradiance (W/m²)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Irradiance (W/m²)': df_chart['irradiance_W_m2']}).set_index('Time'), color="#ea580c", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('sun', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

    with col_sc3:
        # Temperature (°C)
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('thermometer', size=16, color='#dc2626')} Temperature (°C)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Temp (°C)': df_chart['temperature_C']}).set_index('Time'), color="#dc2626", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('thermometer', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

        # Energy (kWh) strictly standardized
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-card-header">
                <span class="chart-header-title">{get_icon('battery-charging', size=16, color='#10b981')} Energy (kWh)</span>
            </div>
            """, unsafe_allow_html=True)
            if not df_chart.empty and len(df_chart) > 0:
                st.line_chart(pd.DataFrame({'Time': df_chart['time_display'], 'Energy (kWh)': df_chart['energy_kWh']}).set_index('Time'), color="#10b981", height=125)
            else:
                st.markdown(f"""
                <div class="chart-empty-state sec-empty">
                    {get_icon('battery-charging', size=16, color='#94a3b8')}
                    <div class="empty-state-title">No telemetry yet</div>
                    <div class="empty-state-sub">Waiting for incoming data...</div>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# ZONE 3 (RIGHT): SYSTEM STATUS, SOLAR CONDITIONS GAUGE, EVENTS & EXPORT
# -----------------------------------------------------------------------------------------
with col_right:
    # 1. System Status Panel (25% Reduced Vertical Spacing, High Density, Semantic Colors)
    logging_status_str = "Active" if solar_data['logging_active'] else "Error"
    logging_status_color = "#047857" if solar_data['logging_active'] else "#b91c1c"
    logging_dot_color = "green" if solar_data['logging_active'] else "red"

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('shield-check', size=16, color='#0f172a')} SYSTEM STATUS</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('activity', size=16, color='#2563eb')} Overall Health</span>
            <span class="status-badge" style="color: {'#047857' if system_normal else '#b45309'};"><span class="status-dot {'green' if system_normal else 'amber'}"></span> {health_status}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('wifi', size=16, color='#059669' if solar_data['mqtt_connected'] else '#ef4444')} MQTT Connection</span>
            <span class="status-badge" style="color: {'#047857' if solar_data['mqtt_connected'] else '#b91c1c'};"><span class="status-dot {'green' if solar_data['mqtt_connected'] else 'red'}"></span> {'Connected' if solar_data['mqtt_connected'] else 'Disconnected'}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('database', size=16, color='#10b981' if solar_data['logging_active'] else '#ef4444')} Data Logging</span>
            <span class="status-badge" style="color: {logging_status_color};"><span class="status-dot {logging_dot_color}"></span> {logging_status_str}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('clock', size=16, color='#64748b')} Last Packet</span>
            <span class="status-badge" style="color: #0f172a;">{freshness_label}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('refresh', size=16, color='#2563eb')} Reconnect Count</span>
            <span class="status-badge" style="color: #2563eb;">{solar_data['reconnect_count']}</span>
        </div>
        <div class="status-row">
            <span class="status-label">{get_icon('layers', size=16, color='#64748b')} Total Messages</span>
            <span class="status-badge" style="color: #475569;">{solar_data['msg_count']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Solar Conditions: Compact Semi-Circular Gauge / Radial Indicator (STC Normalization)
    current_irr = max(0.0, float(solar_data['watts']))
    # Standard STC solar irradiance normalization: 1000 W/m² = 1.0 (1 Sun)
    norm_frac = min(max(current_irr / 1000.0, 0.0), 1.0)
    
    if current_irr < 200.0:
        cond_tier = "Low"
        cond_badge_color = "#0284c7"
        cond_tier_dot = "blue"
    elif current_irr <= 650.0:
        cond_tier = "Moderate"
        cond_badge_color = "#d97706"
        cond_tier_dot = "amber"
    else:
        cond_tier = "Strong"
        cond_badge_color = "#ea580c"
        cond_tier_dot = "orange"

    # Semi-circular geometry: center (100, 75), radius = 56
    gauge_r = 56
    gauge_cx, gauge_cy = 100, 75
    arc_length = math.pi * gauge_r # ~175.93
    dash_offset = arc_length * (1.0 - norm_frac)
    
    # Needle coordinates on arc
    angle_rad = math.pi * (1.0 - norm_frac)
    needle_x = gauge_cx + gauge_r * math.cos(angle_rad)
    needle_y = gauge_cy - gauge_r * math.sin(angle_rad)
    stc_pct_str = f"{(current_irr / 10.0):.1f}% STC"

    st.markdown(f"""
    <div class="glass-card">
        <div class="card-heading">
            <span>{get_icon('sun', size=16, color='#ea580c')} SOLAR CONDITIONS</span>
            <span style="font-size: 10.5px; font-weight: 500; color: #64748b; text-transform: none;">Solar Intensity</span>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 2px 0;">
            <svg viewBox="24 12 152 75" style="width: 100%; max-width: 210px; overflow: visible;">
                <defs>
                    <linearGradient id="solarArcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#38bdf8" />
                        <stop offset="35%" stop-color="#fbbf24" />
                        <stop offset="70%" stop-color="#f97316" />
                        <stop offset="100%" stop-color="#ea580c" />
                    </linearGradient>
                </defs>
                <!-- Background Arc Track -->
                <path d="M 44 75 A 56 56 0 0 1 156 75" fill="none" stroke="#e2e8f0" stroke-width="8" stroke-linecap="round" />
                <!-- Active Solar Radiation Arc -->
                <path d="M 44 75 A 56 56 0 0 1 156 75" fill="none" stroke="url(#solarArcGrad)" stroke-width="8" stroke-linecap="round"
                      stroke-dasharray="{arc_length:.2f}" stroke-dashoffset="{dash_offset:.2f}" />
                <!-- Precision Indicator Bead -->
                <circle cx="{needle_x:.1f}" cy="{needle_y:.1f}" r="5.5" fill="#0f172a" stroke="#ffffff" stroke-width="2" />
                <!-- Center Digital Readouts -->
                <text x="100" y="55" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a" letter-spacing="-0.3px">{current_irr:.1f}</text>
                <text x="100" y="68" text-anchor="middle" font-size="10" font-weight="500" fill="#64748b">W/m²</text>
            </svg>
            <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 210px; margin-top: -1px; padding: 0 4px;">
                <span style="font-size: 10px; font-weight: 500; color: #64748b;">Low</span>
                <span style="display: inline-flex; align-items: center; gap: 5px; font-size: 11px; font-weight: 600; color: {cond_badge_color}; background: rgba(241, 245, 249, 0.9); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(226, 232, 240, 0.9);">
                    <span class="status-dot {cond_tier_dot}"></span> {cond_tier} ({stc_pct_str})
                </span>
                <span style="font-size: 10px; font-weight: 500; color: #64748b;">Strong</span>
            </div>
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
            <span>{get_icon('bell', size=16, color='#0f172a')} RECENT EVENTS</span>
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
# 12. COMPACT ANALYTICAL "PERFORMANCE SNAPSHOT" SECTION (TIMEFRAME-AWARE REAL METRICS)
# =========================================================================================
# Format clean timeframe title dynamically matching selected filter
tf_map = {
    "1 Min": "1 MIN",
    "5 Mins": "5 MIN",
    "15 Mins": "15 MIN",
    "1 Hour": "1 HOUR",
    "12 Hours": "12 HOURS",
    "All-Time": "ALL-TIME"
}
tf_title = tf_map.get(timeframe, timeframe.upper())
snapshot_heading = f"PERFORMANCE SNAPSHOT · {tf_title}"

if not df_chart.empty and len(df_chart) > 0:
    valid_power = df_chart['power_W'].dropna()
    valid_voltage = df_chart['voltage_V'].dropna()
    valid_current = df_chart['current_mA'].dropna()
    valid_irr = df_chart['irradiance_W_m2'].dropna()

    peak_p = valid_power.max() if not valid_power.empty else None
    peak_v = valid_voltage.max() if not valid_voltage.empty else None
    peak_i = valid_current.max() if not valid_current.empty else None
    avg_p = valid_power.mean() if not valid_power.empty else None
    avg_irr = valid_irr.mean() if not valid_irr.empty else None

    peak_p_str = f"{peak_p:.2f} <span class='snapshot-unit'>W</span>" if peak_p is not None else "N/A"
    peak_v_str = f"{peak_v:.2f} <span class='snapshot-unit'>V</span>" if peak_v is not None else "N/A"
    peak_i_str = f"{peak_i:.1f} <span class='snapshot-unit'>mA</span>" if peak_i is not None else "N/A"
    avg_p_str = f"{avg_p:.2f} <span class='snapshot-unit'>W</span>" if avg_p is not None else "N/A"
    avg_irr_str = f"{avg_irr:.1f} <span class='snapshot-unit'>W/m²</span>" if avg_irr is not None else "N/A"
else:
    peak_p_str = "N/A"
    peak_v_str = "N/A"
    peak_i_str = "N/A"
    avg_p_str = "N/A"
    avg_irr_str = "N/A"

st.markdown(f"""
<div class="glass-card" style="margin-top: 2px; margin-bottom: 10px;">
    <div class="card-heading">
        <span>{get_icon('trending-up', size=16, color='#ea580c')} {snapshot_heading}</span>
        <span style="font-size: 10.5px; font-weight: 500; color: #64748b; text-transform: none;">Dynamic Telemetry Analytics</span>
    </div>
    <div class="snapshot-grid">
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('zap', size=16, color='#ea580c')} Peak Power</div>
            <div class="snapshot-val">{peak_p_str}</div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('gauge', size=16, color='#2563eb')} Peak Voltage</div>
            <div class="snapshot-val">{peak_v_str}</div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('activity', size=16, color='#d97706')} Peak Current</div>
            <div class="snapshot-val">{peak_i_str}</div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('activity', size=16, color='#2563eb')} Average Power</div>
            <div class="snapshot-val">{avg_p_str}</div>
        </div>
        <div class="snapshot-card">
            <div class="snapshot-label">{get_icon('sun', size=16, color='#f59e0b')} Average Irradiance</div>
            <div class="snapshot-val">{avg_irr_str}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================================================
# 13. BOTTOM FULL-WIDTH ZONE: RECENT MEASUREMENTS TABLE (W & kWh STANDARDIZED)
# =========================================================================================
col_tbl_head, col_tbl_ctl = st.columns([3, 1])
with col_tbl_head:
    st.markdown(f"""
    <div class="table-header-pill">
        {get_icon('database', size=16, color='#2563eb')}
        <span>Recent Telemetry Measurements</span>
    </div>
    """, unsafe_allow_html=True)
with col_tbl_ctl:
    row_count = st.selectbox("Rows to display", options=[5, 10, 20, 50], index=1)

if solar_data['log_records']:
    df_table = pd.DataFrame(solar_data['log_records'])
    
    # Ensure energy_kWh and power_W are present
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
    st.dataframe(df_display, use_container_width=True, height=195)
else:
    st.info("Waiting for incoming telemetry packets to populate table...")

# =========================================================================================
# 14. LIVE UPDATE AUTO-RERUN LOOP
# =========================================================================================
if live_update:
    time.sleep(3.5)
    st.rerun()