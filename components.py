import streamlit as st
import numpy as np

def get_laser_svg():
    return """
    <svg width="120" height="70" viewBox="0 0 120 70" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="laserGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#444;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#222;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#444;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect x="10" y="15" width="90" height="35" rx="8" fill="url(#laserGrad)" stroke="#000" stroke-width="2"/>
        <rect x="85" y="24" width="20" height="18" rx="2" fill="#1a1a1a" stroke="#000" stroke-width="1"/>
        <circle cx="98" cy="33" r="5" fill="#ff0000" class="glow-red" />
        <text x="50" y="40" font-family="sans-serif" font-size="10" fill="#888" font-weight="bold" text-anchor="middle">LASER</text>
    </svg>
    """

def get_component_svg(label, angle_deg, color="#ffcc00"):
    return f"""
    <div class="component-wrapper">
        <svg width="110" height="130" viewBox="0 0 110 130" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="110" width="100" height="12" rx="2" fill="#333" stroke="#000" stroke-width="2"/>
            <rect x="48" y="70" width="14" height="40" fill="#666" stroke="#222" stroke-width="1"/>
            <circle cx="55" cy="45" r="40" fill="#222" stroke="#444" stroke-width="3"/>
            <g transform="rotate({angle_deg}, 55, 45)">
                <circle cx="55" cy="45" r="32" fill="{color}" fill-opacity="0.2" stroke="{color}" stroke-width="2.5"/>
                <line x1="55" y1="13" x2="55" y2="77" stroke="{color}" stroke-width="3" stroke-dasharray="6,3"/>
                <circle cx="55" cy="18" r="3.5" fill="#fff" stroke="#000" stroke-width="1"/>
            </g>
            <text x="55" y="127" font-family="sans-serif" font-size="11" fill="#eee" font-weight="bold" text-anchor="middle">{label}</text>
        </svg>
    </div>
    """

def get_polarization_state_svg(Ax, Ay, delta, intensity):
    opacity = min(1.0, intensity / 2.0)
    t = np.linspace(0, 2*np.pi, 64)
    Ex = Ax * np.cos(t)
    Ey = Ay * np.cos(t + delta)
    max_val = max(Ax, Ay, 0.001)
    Ex_svg = np.round((Ex / max_val) * 15 + 20, 2)
    Ey_svg = np.round((Ey / max_val) * 15 + 20, 2)
    points = " ".join([f"{x},{y}" for x, y in zip(Ex_svg, Ey_svg)])
    
    return f"""
    <div class="state-container">
        <svg width="40" height="40" viewBox="0 0 40 40">
            <rect width="40" height="40" fill="#444" fill-opacity="0.3" rx="5"/>
            <polyline points="{points}" fill="none" stroke="#00ff00" stroke-width="2" stroke-opacity="{opacity}" />
            <line x1="20" y1="5" x2="20" y2="35" stroke="#666" stroke-width="0.5" stroke-dasharray="2,2"/>
            <line x1="5" y1="20" x2="35" y2="20" stroke="#666" stroke-width="0.5" stroke-dasharray="2,2"/>
        </svg>
    </div>
    """

def get_beam_segment_html(intensity, state_svg=""):
    opacity = max(0.1, min(1.0, intensity / 2.0))
    pulse_class = "beam-pulse" if intensity > 0.01 else ""
    return f"""
    <div class="beam-segment">
        {state_svg}
        <div class="beam-line {pulse_class}" style="opacity: {opacity}; box-shadow: 0 0 {10*opacity}px rgba(255,0,0,0.8);"></div>
    </div>
    """

def get_detector_svg(intensity):
    brightness = min(255, int(intensity * 120))
    color = f"rgb({brightness}, 0, 0)"
    return f"""
    <svg width="110" height="110" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="20" width="90" height="70" rx="10" fill="#2a2a2a" stroke="#000" stroke-width="3"/>
        <rect x="25" y="35" width="60" height="40" rx="3" fill="#111" stroke="#444" stroke-width="1"/>
        <circle cx="55" cy="55" r="15" fill="{color}" class="glow-red" />
        <text x="55" y="102" font-family="sans-serif" font-size="11" fill="#eee" font-weight="bold" text-anchor="middle">DETECTOR</text>
    </svg>
    """

def get_bench_styles():
    return """
    <style>
    body { margin: 0; padding: 0; font-family: sans-serif; background: transparent; overflow-x: auto; }
    .bench-container {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background: #1e1e1e;
        padding: 40px 20px;
        border-radius: 15px;
        border: 1px solid #444;
        min-height: 220px;
        min-width: fit-content;
    }
    .component-wrapper { display: flex; align-items: center; }
    .beam-segment {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100px;
        flex-shrink: 0;
    }
    .beam-line {
        width: 100%;
        height: 6px;
        background: red;
        border-radius: 3px;
        margin-top: 10px;
    }
    .beam-pulse {
        animation: pulse 1.5s infinite alternate;
    }
    @keyframes pulse {
        from { opacity: 0.4; }
        to { opacity: 1.0; box-shadow: 0 0 15px rgba(255,0,0,1); }
    }
    .glow-red {
        filter: drop-shadow(0 0 5px red);
    }
    .state-container { margin-bottom: 5px; }
    </style>
    """
