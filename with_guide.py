import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

import os

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Polarization Optics Visual Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Helper: read the explainer HTML for inline rendering ─────────────────────
def _load_explainer_html() -> str:
    """Read polarization_explainer.html from the same directory as this script."""
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "polarization_explainer.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<p style='color:red'>polarization_explainer.html not found.</p>"


BG = '#080c14'
FG = '#c9d4e8'
ACCENT  = '#38bdf8'
ACCENT2 = '#818cf8'
ACCENT3 = '#f472b6'
GRID    = '#0f1f35'
HTML_BG = '#07101f'

# ── Theory Guide Dialog ──────────────────────────────────────────────────────
@st.dialog("Theory Guide: Polarization Optics", width="large")
def show_theory_dialog():
    html_content = _load_explainer_html()
    # Add a bit of padding/styling for the dialog container if needed
    components.html(html_content, height=800, scrolling=True)

st.markdown("""
<style>
  :root {
    --c-bg: #080c14;
    --c-text: #c9d4e8;
    --c-sb-bg: linear-gradient(180deg, #0d1421 0%, #0a1628 100%);
    --c-brd: #1e3a5f;
    --c-sb-text: #a8c0de;
    --c-grad: linear-gradient(135deg, #38bdf8, #818cf8, #f472b6);
    --c-h2: #38bdf8;
    --c-h3: #818cf8;
    --c-card: linear-gradient(135deg, #0f1f35, #0d1928);
    --c-card-l: #4a7fa5;
    --c-card-v: #38bdf8;
    --c-card-s: #5a8fa8;
    --c-tab-th: #0f1f35;
    --c-tab-o: #080c14;
    --c-tab-e: #0a1520;
    --c-info: linear-gradient(135deg, #0a1e35, #081428);
    --c-info-t: #8ab4d4;
    --c-form: #080c14;
    --c-script: #050a12;
    --c-scrt-t: #8ab4d4;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Syne:wght@400;700;800&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: var(--c-bg);
    color: var(--c-text);
  }
  .stApp { background: var(--c-bg); }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: var(--c-sb-bg);
    border-right: 1px solid var(--c-brd);
  }
  section[data-testid="stSidebar"] * { color: var(--c-sb-text) !important; }
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stSlider label { color: var(--c-text) !important; font-size: 0.78rem !important; }

  /* Headers */
  h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important;
       background: var(--c-grad);
       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
       letter-spacing: -1px; font-size: 2.4rem !important; }
  h2 { font-family: 'Syne', sans-serif !important; color: var(--c-h2) !important;
       font-size: 1.1rem !important; letter-spacing: 2px; text-transform: uppercase;
       border-bottom: 1px solid var(--c-brd); padding-bottom: 6px; }
  h3 { font-family: 'Syne', sans-serif !important; color: var(--c-h3) !important;
       font-size: 0.95rem !important; }

  /* Metric cards */
  .metric-card {
    background: var(--c-card);
    border: 1px solid var(--c-brd);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
  }
  .metric-label { font-size: 0.68rem; color: var(--c-card-l); letter-spacing: 2px; text-transform: uppercase; }
  .metric-value { font-size: 1.5rem; font-weight: 600; color: var(--c-card-v); font-family: 'JetBrains Mono'; }
  .metric-sub   { font-size: 0.72rem; color: var(--c-card-s); }

  /* Pipeline */
  .pipeline-box {
    background: var(--c-card);
    border: 1px solid var(--c-brd);
    border-radius: 10px;
    padding: 18px;
    margin: 10px 0;
    text-align: center;
  }
  .pipeline-icon { font-size: 2rem; }
  .pipeline-label { font-size: 0.7rem; color: var(--c-card-v); letter-spacing: 2px; text-transform: uppercase; margin-top: 4px; }

  /* Tables */
  .hw-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  .hw-table th { background: var(--c-tab-th); color: var(--c-card-v); padding: 8px 12px;
                 text-align: left; border-bottom: 1px solid var(--c-brd); }
  .hw-table td { padding: 8px 12px; border-bottom: 1px solid var(--c-tab-th); }
  .hw-table tr:nth-child(even) td { background: var(--c-tab-e); }
  .hw-table tr:nth-child(odd) td { background: var(--c-tab-o); }

  /* Info box */
  .info-box {
    background: var(--c-info);
    border-left: 3px solid var(--c-card-v);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.8rem;
    color: var(--c-info-t);
  }
  .formula { font-family: 'JetBrains Mono'; color: var(--c-h3); font-size: 0.85rem;
             background: var(--c-form); padding: 8px 14px; border-radius: 6px;
             border: 1px solid var(--c-brd); margin: 6px 0; display: inline-block; }

  /* Stokes bar */
  .stokes-bar-bg { background: var(--c-tab-th); border-radius: 4px; height: 8px; margin: 4px 0; }
  .stokes-bar-fill { height: 8px; border-radius: 4px; transition: width 0.3s; }

  /* Script box */
  .script-box {
    background: var(--c-script);
    border: 1px solid var(--c-brd);
    border-radius: 10px;
    padding: 20px;
    font-size: 0.82rem;
    color: var(--c-scrt-t);
    line-height: 1.7;
  }
  .script-time { color: var(--c-card-v); font-weight: 600; }

  div[data-testid="stMetricValue"] { color: var(--c-card-v) !important; font-family: 'JetBrains Mono' !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  PHYSICS ENGINE  ░░
# ─────────────────────────────────────────────────────────────────────────────

def jones_vector(polarization: str, phase_deg: float = 0.0) -> np.ndarray:
    """
    Return the Jones vector (2-element complex array) for the chosen input state.

    polarization : 'linear_0'  — horizontal (0°)
                   'linear_45' — 45° linear
                   'linear_90' — vertical (90°)
                   'lcp'       — left circular
                   'rcp'       — right circular
                   'elliptical'— elliptical, controlled by phase_deg
    phase_deg    : phase delay δ (degrees) used only for 'elliptical'
    """
    # Process in degrees directly
    states = {
        'linear_0':   np.array([1.0 + 0j, 0.0 + 0j]),
        'linear_45':  np.array([1.0, 1.0]) / np.sqrt(2),
        'linear_90':  np.array([0.0 + 0j, 1.0 + 0j]),
        'lcp':        np.array([1.0, -1j]) / np.sqrt(2),
        'rcp':        np.array([1.0,  1j]) / np.sqrt(2),
        'elliptical': np.array([np.cos(np.deg2rad(45)),
                                np.sin(np.deg2rad(45)) * np.exp(1j * np.deg2rad(phase_deg))]),
    }
    return states[polarization]


def polarizer_matrix(theta_deg: float) -> np.ndarray:
    """
    Jones matrix for an ideal linear polarizer at angle θ (degrees).

    M = R(-θ) · [[1,0],[0,0]] · R(θ)
    """
    θ = theta_deg
    c, s = np.cos(np.deg2rad(θ)), np.sin(np.deg2rad(θ))
    return np.array([[c**2,      c * s],
                     [c * s,     s**2]], dtype=complex)


def waveplate_matrix(phase_deg: float, fast_axis_deg: float = 0.0) -> np.ndarray:
    """
    Jones matrix for a wave plate.

    phase_deg     : retardation in degrees (90 = QWP, 180 = HWP)
    fast_axis_deg : orientation of the fast axis (degrees)

    Formula: R(-α) · [[e^{-iΓ/2}, 0],[0, e^{iΓ/2}]] · R(α)
    """
    Γ = phase_deg
    α = fast_axis_deg
    c, s = np.cos(np.deg2rad(α)), np.sin(np.deg2rad(α))
    # Rotation matrix
    R  = np.array([[c, s], [-s, c]], dtype=complex)
    Ri = np.array([[c, -s], [s, c]], dtype=complex)
    # Phase matrix (fast axis along x)
    P  = np.array([[np.exp(-1j * np.deg2rad(Γ) / 2), 0],
                   [0,  np.exp( 1j * np.deg2rad(Γ) / 2)]], dtype=complex)
    return Ri @ P @ R


def compute_output(E_in: np.ndarray,
                   polarizer_angle: float,
                   use_qwp: bool,
                   use_hwp: bool,
                   analyzer_angle: float,
                   qwp_axis: float = 45.0,
                   hwp_axis: float = 22.5) -> tuple:
    """
    Propagate E_in through the optical pipeline and return (E_out, intensity).

    Pipeline: E_in → Polarizer → [QWP] → [HWP] → Analyzer
    """
    E = polarizer_matrix(polarizer_angle) @ E_in

    if use_qwp:
        E = waveplate_matrix(90.0, fast_axis_deg=qwp_axis) @ E

    if use_hwp:
        E = waveplate_matrix(180.0, fast_axis_deg=hwp_axis) @ E

    E_out = polarizer_matrix(analyzer_angle) @ E
    intensity = float(np.abs(E_out[0])**2 + np.abs(E_out[1])**2)
    return E_out, intensity


def compute_stokes(E: np.ndarray) -> dict:
    """
    Compute the four Stokes parameters from a Jones vector.

    S0 = |Ex|² + |Ey|²           (total intensity)
    S1 = |Ex|² − |Ey|²           (horizontal vs vertical)
    S2 = 2·Re(Ex·Ey*)            (diagonal linear)
    S3 = 2·Im(Ex·Ey*)            (circular component)
    """
    Ex, Ey = E[0], E[1]
    S0 = float(np.abs(Ex)**2 + np.abs(Ey)**2)
    S1 = float(np.abs(Ex)**2 - np.abs(Ey)**2)
    S2 = float(2 * np.real(Ex * np.conj(Ey)))
    S3 = float(2 * np.imag(Ex * np.conj(Ey)))
    return {'S0': S0, 'S1': S1, 'S2': S2, 'S3': S3}


def jones_after_polarizer(E_in: np.ndarray,
                           polarizer_angle: float,
                           use_qwp: bool,
                           use_hwp: bool,
                           qwp_axis: float = 45.0,
                           hwp_axis: float = 22.5) -> np.ndarray:
    """Return the Jones vector just before the analyzer (for ellipse display)."""
    E = polarizer_matrix(polarizer_angle) @ E_in
    if use_qwp:
        E = waveplate_matrix(90.0, fast_axis_deg=qwp_axis) @ E
    if use_hwp:
        E = waveplate_matrix(180.0, fast_axis_deg=hwp_axis) @ E
    return E


# ─────────────────────────────────────────────────────────────────────────────
# ░░  MATPLOTLIB FIGURES  ░░
# ─────────────────────────────────────────────────────────────────────────────

BG = '#080c14'
FG = '#c9d4e8'
ACCENT  = '#38bdf8'
ACCENT2 = '#818cf8'
ACCENT3 = '#f472b6'
GRID    = '#0f1f35'


def _fig_style(fig, ax=None):
    fig.patch.set_facecolor(BG)
    if ax:
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(ACCENT)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.7)


def animate_polarization(E: np.ndarray, n_frames: int = 300) -> plt.Figure:
    """
    Draw the polarization ellipse (Ex vs Ey trace over one full cycle)
    plus a moving dot showing the current tip of the E-field vector.
    """
    Ex_amp = np.abs(E[0])
    Ey_amp = np.abs(E[1])
    # Compute phase in degrees and trace ellipse using degrees
    δx_deg = np.degrees(np.angle(E[0]))
    δy_deg = np.degrees(np.angle(E[1]))
    t_deg  = np.linspace(0, 360, n_frames)

    Ex = Ex_amp * np.cos(np.deg2rad(t_deg + δx_deg))
    Ey = Ey_amp * np.cos(np.deg2rad(t_deg + δy_deg))

    # Animated dot position (25% into cycle)
    dot_idx = n_frames // 4
    dot_x, dot_y = Ex[dot_idx], Ey[dot_idx]

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    _fig_style(fig, ax)

    # Faded outer ellipse
    ax.plot(Ex, Ey, color=ACCENT, lw=1.5, alpha=0.35)
    # Gradient-coloured full trace using line segments
    from matplotlib.collections import LineCollection
    pts = np.array([Ex, Ey]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, linewidths=2,
                        colors=[plt.cm.cool(i / n_frames) for i in range(len(segs))])
    ax.add_collection(lc)

    # Axes arrows
    ax.axhline(0, color=GRID, lw=0.8)
    ax.axvline(0, color=GRID, lw=0.8)

    # Moving dot + lines to axes
    ax.plot(dot_x, dot_y, 'o', color=ACCENT3, markersize=9, zorder=5)
    ax.plot([dot_x, dot_x], [0, dot_y], '--', color=ACCENT3, lw=0.8, alpha=0.6)
    ax.plot([0, dot_x],     [dot_y, dot_y], '--', color=ACCENT3, lw=0.8, alpha=0.6)

    lim = max(Ex_amp, Ey_amp) * 1.3 + 0.1
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel('Ex', fontsize=9)
    ax.set_ylabel('Ey', fontsize=9)
    ax.set_title('Polarization Graph', fontsize=10, pad=8)
    ax.set_aspect('equal')
    fig.tight_layout(pad=1.0)
    return fig


def intensity_vs_analyzer(E_in: np.ndarray,
                           polarizer_angle: float,
                           use_qwp: bool,
                           use_hwp: bool,
                           current_analyzer: float) -> plt.Figure:
    """
    Plot intensity as the analyzer is rotated 0–360°.
    Also mark the current analyzer angle with a vertical line.
    """
    angles   = np.linspace(0, 360, 720)
    intensities = []
    for a in angles:
        _, I = compute_output(E_in, polarizer_angle, use_qwp, use_hwp, a)
        intensities.append(I)

    fig, ax = plt.subplots(figsize=(6, 3))
    _fig_style(fig, ax)

    ax.fill_between(angles, intensities, alpha=0.15, color=ACCENT)
    ax.plot(angles, intensities, color=ACCENT, lw=2, label='I(θ)')

    # Cosine² reference (Malus' law from initial)
    I0 = max(intensities) if max(intensities) > 0 else 1
    ref = I0 * np.cos(np.deg2rad(angles - polarizer_angle))**2
    ax.plot(angles, ref, '--', color=ACCENT2, lw=1, alpha=0.5, label='cos²(θ) ref')

    # Current analyzer marker
    _, cur_I = compute_output(E_in, polarizer_angle, use_qwp, use_hwp, current_analyzer)
    ax.axvline(current_analyzer, color=ACCENT3, lw=1.5, alpha=0.9, ls='--')
    ax.plot(current_analyzer, cur_I, 'o', color=ACCENT3, markersize=7, zorder=5)

    ax.set_xlabel('Analyzer Angle (°)', fontsize=9)
    ax.set_ylabel('Intensity (a.u.)', fontsize=9)
    ax.set_title('Intensity vs Analyzer Angle', fontsize=10, pad=8)
    ax.set_xlim(0, 360)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(fontsize=7, loc='upper right',
              facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.0)
    return fig


def stokes_sphere_projection(stokes: dict) -> plt.Figure:
    """
    Project the Poincaré sphere state as a 2D S1-S2-S3 bar chart
    and draw a small indicator on the (S1,S2) plane.
    """
    S0, S1, S2, S3 = stokes['S0'], stokes['S1'], stokes['S2'], stokes['S3']
    safe = S0 if S0 > 1e-9 else 1.0
    s1n, s2n, s3n = S1 / safe, S2 / safe, S3 / safe

    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3),
                             gridspec_kw={'width_ratios': [1.6, 1]})
    _fig_style(fig, axes[0])
    _fig_style(fig, axes[1])

    # Bar chart of normalised Stokes
    labels  = ['s₁', 's₂', 's₃']
    vals    = [s1n, s2n, s3n]
    colors  = [ACCENT, ACCENT2, ACCENT3]
    bars = axes[0].bar(labels, vals, color=colors, alpha=0.85, width=0.45)
    axes[0].axhline(0, color=GRID, lw=0.8)
    axes[0].set_ylim(-1.1, 1.1)
    axes[0].set_title('Normalised Stokes (s₁ s₂ s₃)', fontsize=9, pad=6)
    for bar, val in zip(bars, vals):
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     val + (0.05 if val >= 0 else -0.12),
                     f'{val:.2f}', ha='center', va='bottom',
                     fontsize=8, color=FG)

    # Simple Poincaré circle (S1-S2 plane)
    np.random.seed(42) # just for stable linspace degree usage
    θ_p_deg = np.linspace(0, 360, 200)
    axes[1].plot(np.cos(np.deg2rad(θ_p_deg)), np.sin(np.deg2rad(θ_p_deg)), color=GRID, lw=1)
    axes[1].axhline(0, color=GRID, lw=0.5)
    axes[1].axvline(0, color=GRID, lw=0.5)
    axes[1].plot(s1n, s2n, 'o', color=ACCENT3, markersize=9, zorder=5)
    axes[1].set_xlim(-1.3, 1.3)
    axes[1].set_ylim(-1.3, 1.3)
    axes[1].set_title('S₁-S₂ Poincaré', fontsize=9, pad=6)
    axes[1].set_xlabel('S₁', fontsize=8)
    axes[1].set_ylabel('S₂', fontsize=8)
    axes[1].set_aspect('equal')

    fig.tight_layout(pad=1.0)
    return fig


def animated_pipeline_html(E_stages: list, use_qwp: bool, use_hwp: bool, intensity: float,
                           pol_angle: float, qwp_axis: float, hwp_axis: float, analyzer_angle: float) -> str:
    """
    Build a self-contained HTML/Canvas animation showing live electromagnetic
    waves travelling through each optical element.

    E_stages : list of 6 complex numpy arrays [Ein, Epol, Eqwp, Ehwp, Eana, Eout]
               Each entry is shape (2,) complex — [Ex, Ey].
               Pass None for inactive stages (QWP/HWP when off).
    """
    import json

    def stage_params(E):
        if E is None:
            return {"ExA": 0, "EyA": 0, "dX": 0, "dY": 0}
        ExA = float(np.abs(E[0]))
        EyA = float(np.abs(E[1]))
        dX  = float(np.degrees(np.angle(E[0])))
        dY  = float(np.degrees(np.angle(E[1])))
        return {"ExA": ExA, "EyA": EyA, "dX": dX, "dY": dY}

    stages_json = json.dumps([stage_params(e) for e in E_stages])
    angles_json = json.dumps({
        "POLARIZER": float(pol_angle),
        "QWP": float(qwp_axis),
        "HWP": float(hwp_axis),
        "ANALYZER": float(analyzer_angle)
    })
    qwp_js  = "true" if use_qwp  else "false"
    hwp_js  = "true" if use_hwp  else "false"
    int_js  = f"{intensity:.4f}"

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: {HTML_BG}; font-family: 'Courier New', monospace; color: {FG}; }}
  canvas {{ display: block; width: 100%; }}
  .legend {{
    display: flex; gap: 20px; padding: 6px 12px;
    background: {HTML_BG}; border-top: 1px solid {GRID};
  }}
  .leg-item {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #4a7fa5; }}
  .leg-dot {{ width: 28px; height: 3px; border-radius: 2px; }}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div class="legend">
  <div class="leg-item"><div class="leg-dot" style="background:#38bdf8"></div>Ex component</div>
  <div class="leg-item"><div class="leg-dot" style="background:#f472b6"></div>Ey component</div>
  <div class="leg-item"><div class="leg-dot" style="background:#fbbf24;height:2px;border:1px dashed #fbbf24;background:none"></div>beam axis</div>
</div>
<script>
// Degree based trig helpers
const cosDeg = d => Math.cos(d * Math.PI / 180);
const sinDeg = d => Math.sin(d * Math.PI / 180);

const cv = document.getElementById('c');
const ctx = cv.getContext('2d');
const stages = {stages_json};
const angles = {angles_json};
const useQwp = {qwp_js};
const useHwp = {hwp_js};
const intensity = {int_js};

// canvas sizing
function resize() {{
  cv.width  = cv.offsetWidth  * (window.devicePixelRatio || 1);
  cv.height = 340             * (window.devicePixelRatio || 1);
  ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
}}
resize();
window.addEventListener('resize', () => {{ resize(); }});

const W = () => cv.offsetWidth;
const H = 340;

// element definitions
const ELEMS = [
  {{ label:'LASER',    color:'#f59e0b', always:true  }},
  {{ label:'POLARIZER',color:'#38bdf8', always:true  }},
  {{ label:'QWP',      color:'#818cf8', always:false, flag: useQwp }},
  {{ label:'HWP',      color:'#a78bfa', always:false, flag: useHwp }},
  {{ label:'ANALYZER', color:'#34d399', always:true  }},
  {{ label:'SENSOR',   color:'#f472b6', always:true  }},
];

// wave segment between elements i and i+1
// uses stage[i] params
const WAVE_STAGE = [0, 1, 2, 3, 4]; // 5 gaps for 6 elements

let t = 0;

function isActive(i) {{
  if (ELEMS[i].always) return true;
  return ELEMS[i].flag;
}}

function roundRect(ctx, x, y, w, h, r) {{
  ctx.beginPath();
  ctx.moveTo(x+r, y);
  ctx.lineTo(x+w-r, y); ctx.arcTo(x+w, y, x+w, y+r, r);
  ctx.lineTo(x+w, y+h-r); ctx.arcTo(x+w, y+h, x+w-r, y+h, r);
  ctx.lineTo(x+r, y+h); ctx.arcTo(x, y+h, x, y+h-r, r);
  ctx.lineTo(x, y+r); ctx.arcTo(x, y, x+r, y, r);
  ctx.closePath();
}}

function drawEllipseMini(cx, cy, s, active) {{
  const R = 22;
  ctx.save();
  ctx.globalAlpha = active ? 0.9 : 0.2;

  // circle guide
  ctx.strokeStyle = '#1e3a5f';
  ctx.lineWidth = 0.8;
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI*2); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx-R-3, cy); ctx.lineTo(cx+R+3, cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx, cy-R-3); ctx.lineTo(cx, cy+R+3); ctx.stroke();

  if (s.ExA < 0.01 && s.EyA < 0.01) {{ ctx.restore(); return; }}

  // ellipse trace
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  for (let i = 0; i <= 360; i += 3) {{
    const ex = cx + s.ExA * R * cosDeg(i + s.dX);
    const ey = cy - s.EyA * R * cosDeg(i + s.dY);
    i === 0 ? ctx.moveTo(ex, ey) : ctx.lineTo(ex, ey);
  }}
  ctx.stroke();

  // moving dot
  const dotT = t * 50; // time in degrees
  const dx = cx + s.ExA * R * cosDeg(dotT + s.dX);
  const dy = cy - s.EyA * R * cosDeg(dotT + s.dY);
  ctx.beginPath(); ctx.arc(dx, dy, 3.5, 0, Math.PI*2);
  ctx.fillStyle = '#f472b6'; ctx.fill();

  ctx.restore();
}}

function drawWaveSegment(x0, x1, midY, s, active, phaseShift) {{
  if (!active || (s.ExA < 0.01 && s.EyA < 0.01)) {{
    // dim dashed line if inactive
    ctx.save();
    ctx.globalAlpha = 0.1;
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 6]);
    ctx.beginPath(); ctx.moveTo(x0, midY); ctx.lineTo(x1, midY); ctx.stroke();
    ctx.restore();
    return;
  }}

  const steps = 160;
  const W = x1 - x0;
  const amp = 36;

  // Ex wave
  if (s.ExA > 0.01) {{
    ctx.save();
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2.2;
    ctx.shadowColor = '#38bdf8';
    ctx.shadowBlur = 6;
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {{
      const xp = x0 + i/steps * W;
      // Phase shifts in degrees
      const wt = (t * 50 + phaseShift) - (i/steps) * 720;
      const yp = midY - amp * s.ExA * cosDeg(wt + s.dX);
      i === 0 ? ctx.moveTo(xp, yp) : ctx.lineTo(xp, yp);
    }}
    ctx.stroke();
    ctx.restore();
  }}

  // Ey wave (offset + different color)
  if (s.EyA > 0.02) {{
    ctx.save();
    ctx.strokeStyle = '#f472b6';
    ctx.lineWidth = 2.2;
    ctx.shadowColor = '#f472b6';
    ctx.shadowBlur = 6;
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {{
      const xp = x0 + i/steps * W;
      const wt = (t * 50 + phaseShift) - (i/steps) * 720;
      const yp = midY - amp * s.EyA * cosDeg(wt + s.dY);
      i === 0 ? ctx.moveTo(xp, yp) : ctx.lineTo(xp, yp);
    }}
    ctx.stroke();
    ctx.restore();
  }}

  // travelling bright dot (Ex)
  if (s.ExA > 0.01) {{
    const prog = ((t * 28.647) % 360) / 360; // 0 to 1 progress
    const dotX = x0 + prog * W;
    const wt2 = (t * 50) - prog * 720;
    const dotY = midY - amp * s.ExA * cosDeg(wt2 + s.dX);
    ctx.save();
    ctx.beginPath(); ctx.arc(dotX, dotY, 5, 0, Math.PI*2);
    ctx.fillStyle = '#38bdf8';
    ctx.shadowColor = '#38bdf8'; ctx.shadowBlur = 12;
    ctx.fill();
    ctx.restore();
  }}
}}

function drawElement(x, y, w, h, label, color, active, s) {{
  ctx.save();
  ctx.globalAlpha = active ? 1.0 : 0.22;

  // glow border
  ctx.shadowColor = color;
  ctx.shadowBlur  = active ? 14 : 0;
  ctx.strokeStyle = color;
  ctx.lineWidth   = active ? 2 : 1;
  ctx.fillStyle   = color + '18';
  roundRect(ctx, x, y, w, h, 10);
  ctx.fill();
  ctx.stroke();

  // inner icon
  ctx.shadowBlur = 0;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  const cx = x + w/2, cy = y + h/2;

  ctx.save();
  if (angles[label] !== undefined) {{
    ctx.translate(cx, cy);
    // Usually physics angles are counter-clockwise, canvas is clockwise.
    ctx.rotate(-angles[label] * Math.PI / 180);
    ctx.translate(-cx, -cy);
  }}

  if (label === 'LASER') {{
    // concentric rings
    for (let r = 8; r <= 20; r += 6) {{
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.stroke();
    }}
    // beam arrow out
    ctx.beginPath(); ctx.moveTo(cx+20, cy); ctx.lineTo(cx+w/2-6, cy); ctx.stroke();
  }} else if (label === 'POLARIZER' || label === 'ANALYZER') {{
    // cross-hair with diagonal
    ctx.beginPath(); ctx.moveTo(cx-14, cy); ctx.lineTo(cx+14, cy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx, cy-14); ctx.lineTo(cx, cy+14); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-10, cy-10); ctx.lineTo(cx+10, cy+10); ctx.stroke();
  }} else if (label === 'QWP' || label === 'HWP') {{
    // parallel lines = wave plate
    for (let dy = -10; dy <= 10; dy += 7) {{
      ctx.beginPath(); ctx.moveTo(cx-14, cy+dy); ctx.lineTo(cx+14, cy+dy); ctx.stroke();
    }}
  }} else if (label === 'SENSOR') {{
    // Draw the polarization ellipse on the sensor itself
    const R = 18;
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI*2); 
    ctx.strokeStyle = '#1e3a5f'; ctx.stroke(); // faint guide
    
    if (s && (s.ExA > 0.01 || s.EyA > 0.01)) {{
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let i = 0; i <= 360; i += 4) {{
        const ex = cx + s.ExA * R * cosDeg(i + s.dX);
        const ey = cy - s.EyA * R * cosDeg(i + s.dY);
        i === 0 ? ctx.moveTo(ex, ey) : ctx.lineTo(ex, ey);
      }}
      ctx.stroke();
      
      const dotT = t * 50;
      const dx = cx + s.ExA * R * cosDeg(dotT + s.dX);
      const dy = cy - s.EyA * R * cosDeg(dotT + s.dY);
      ctx.beginPath(); ctx.arc(dx, dy, 2.5, 0, Math.PI*2);
      ctx.fillStyle = '#f472b6'; ctx.fill();
    }}
  }}
  ctx.restore();

  // label inside for wave plates (unrotated)
  if (label === 'QWP' || label === 'HWP') {{
    ctx.fillStyle = color;
    ctx.font = 'bold 9px Courier New';
    ctx.textAlign = 'center';
    ctx.fillText(label === 'QWP' ? 'λ/4' : 'λ/2', cx, cy+22);
  }}

  // label below box
  ctx.shadowBlur = 0;
  ctx.fillStyle  = color;
  ctx.font       = 'bold 10px Courier New';
  ctx.textAlign  = 'center';
  ctx.globalAlpha = active ? 1 : 0.3;
  ctx.fillText(label, cx, y + h + 16);

  // intensity readout on sensor
  if (label === 'SENSOR' && active) {{
    ctx.fillStyle = color;
    ctx.font = '10px Courier New';
    ctx.globalAlpha = 1;
    ctx.fillText('I=' + intensity.toFixed(3), cx, y - 6);
  }}

  ctx.restore();
}}

function frame() {{
  const cw = W(), ch = H;
  ctx.clearRect(0, 0, cw, ch);
  ctx.fillStyle = '{HTML_BG}';
  ctx.fillRect(0, 0, cw, ch);

  // layout
  const elW = 58, elH = 76;
  const totalEl = 6;
  const spacing = (cw - totalEl * elW) / (totalEl + 1);
  const elXs = Array.from({{length: totalEl}}, (_, i) => spacing + i*(elW+spacing));
  const midY = ch * 0.42;
  const elY  = midY - elH * 0.5;
  const ellY = ch - 44;

  // beam axis dashed line
  ctx.save();
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 0.8;
  ctx.globalAlpha = 0.18;
  ctx.setLineDash([6, 8]);
  ctx.beginPath();
  ctx.moveTo(elXs[0] + elW, midY);
  ctx.lineTo(elXs[5], midY);
  ctx.stroke();
  ctx.restore();

  // wave segments between elements
  for (let i = 0; i < 5; i++) {{
    const x0 = elXs[i] + elW + 2;
    const x1 = elXs[i+1] - 2;
    const s  = stages[i];          // stage i params drive segment i→i+1
    const active = isActive(i) && isActive(i+1);
    drawWaveSegment(x0, x1, midY, s, active, i * 22.9); // Phase shift in degrees
  }}

  // elements
  for (let i = 0; i < totalEl; i++) {{
    drawElement(elXs[i], elY, elW, elH, ELEMS[i].label, ELEMS[i].color, isActive(i), stages[i] || stages[0]);
  }}

  // polarization ellipses below each element
  for (let i = 0; i < totalEl; i++) {{
    drawEllipseMini(elXs[i] + elW/2, ellY, stages[i] || stages[0], isActive(i));
  }}

  // ellipse section label
  ctx.save();
  ctx.fillStyle = '{FG}';
  ctx.font = '10px Courier New';
  ctx.textAlign = 'left';
  ctx.fillText('polarization graph at each stage:', 8, ellY - 28);
  ctx.restore();

  t += 0.055;
  requestAnimationFrame(frame);
}}
frame();
</script>
</body>
</html>
"""
    return html


# ─────────────────────────────────────────────────────────────────────────────
# ░░  SIDEBAR — CONTROLS  ░░
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    # ── Theory link ──────────────────────────────────────────
    if st.button("📖 &nbsp; Theory Guide", use_container_width=True, type="primary"):
         show_theory_dialog()

    st.markdown("## ⚙️ Controls")

    if st.button("💡 Replay Tour", use_container_width=True):
        components.html("""<script>window.parent.localStorage.removeItem("tour_done"); window.parent.location.reload();</script>""", height=0, width=0)


    # ── Mode ──────────────────────────────────────────────
    st.markdown("### Mode")
    mode = st.radio("", ['Simulation', 'Hardware + Malus Law'],
                    label_visibility='collapsed')

    st.markdown("---")

    # ── Input Light ───────────────────────────────────────
    st.markdown("### Input Light")
    pol_choice = st.selectbox("Polarization State", [
        'linear_0   — Horizontal (0°)',
        'linear_45  — Diagonal (45°)',
        'linear_90  — Vertical (90°)',
        'lcp        — Left Circular',
        'rcp        — Right Circular',
        'elliptical — Custom Phase',
    ])
    pol_key = pol_choice.split()[0]

    elliptical_phase = 0.0
    if pol_key == 'elliptical':
        elliptical_phase = st.slider("Phase δ (°)", 0, 360, 45, 5)

    st.markdown("---")

    # ── Optical Components ────────────────────────────────
    st.markdown("### Optical Components")
    pol_angle = st.slider("Polarizer Angle (°)", 0, 180, 0, 1)

    col_q, col_h = st.columns(2)
    with col_q:
        use_qwp = st.toggle("QWP", value=False)
    with col_h:
        use_hwp = st.toggle("HWP", value=False)

    qwp_axis = 45.0
    hwp_axis = 22.5
    if use_qwp:
        qwp_axis = st.slider("QWP Fast Axis (°)", 0, 180, 45, 1)
    if use_hwp:
        hwp_axis = st.slider("HWP Fast Axis (°)", 0, 180, 22, 1)

    analyzer_angle = st.slider("Analyzer Angle (°)", 0, 360, 90, 1)

    st.markdown("---")
    st.markdown('<div class="info-box">🔗 Pipeline<br>'
                '<code>Laser → Polarizer → QWP → HWP → Analyzer → Sensor</code></div>',
                unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ░░  COMPUTE  ░░
# ─────────────────────────────────────────────────────────────────────────────

E_in   = jones_vector(pol_key, elliptical_phase)
E_mid  = jones_after_polarizer(E_in, pol_angle, use_qwp, use_hwp, qwp_axis, hwp_axis)
E_out, intensity = compute_output(
    E_in, pol_angle, use_qwp, use_hwp, analyzer_angle, qwp_axis, hwp_axis)
stokes = compute_stokes(E_mid)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  MAIN CONTENT  ░░
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("# 🔬 Polarization Optics Visual Lab")
st.markdown('<p style="color:#4a7fa5;font-size:0.82rem;letter-spacing:2px;'
            'text-transform:uppercase;margin-top:-14px">'
            'Jones Calculus · Wave Plates · Malus Law · Stokes Parameters</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ── Animated Wave Pipeline ────────────────────────────────────────────────────
st.markdown("## Hardware Pipeline — Live Wave Animation")

# Calculated parameters for display
J_out = E_mid
Ax_out = np.abs(J_out[0])
Ay_out = np.abs(J_out[1])
# Calculate phase difference delta = phase(Ey) - phase(Ex)
delta_out = np.angle(J_out[1]) - np.angle(J_out[0])
delta_deg = float(np.degrees(delta_out) % 360)

# Build per-stage Jones vectors for the animation
E_s0 = jones_vector(pol_key, elliptical_phase)                          # laser out
E_s1 = polarizer_matrix(pol_angle) @ E_s0                              # after polarizer
E_s2 = (waveplate_matrix(90.0,  fast_axis_deg=qwp_axis) @ E_s1) if use_qwp else E_s1
E_s3 = (waveplate_matrix(180.0, fast_axis_deg=hwp_axis) @ E_s2) if use_hwp else E_s2
E_s4 = polarizer_matrix(analyzer_angle) @ E_s3                         # after analyzer
E_s5 = E_s4                                                             # at sensor

pipeline_stages = [E_s0, E_s1, E_s2, E_s3, E_s4, E_s5]
anim_html = animated_pipeline_html(pipeline_stages, use_qwp, use_hwp, intensity,
                                   pol_angle, qwp_axis, hwp_axis, analyzer_angle)
components.html(anim_html, height=390, scrolling=False)

# ── Real-time Parameters ──────────────────────────────────────────────────────
st.markdown("## Real-Time Parameters")

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
params = [
    (c1, "Intensity",  f"{intensity:.4f}", "a.u."),
    (c2, "Ax", f"{Ax_out:.2f}", "Amplitude X"),
    (c3, "Ay", f"{Ay_out:.2f}", "Amplitude Y"),
    (c4, "Phase Δ", f"{delta_deg:.1f}°", "Phase Difference"),
    (c5, "S₁ (H/V)",   f"{stokes['S1']:+.3f}", "linear H-V"),
    (c6, "S₂ (Diag)",  f"{stokes['S2']:+.3f}", "linear ±45°"),
    (c7, "S₃ (Circ)",  f"{stokes['S3']:+.3f}", "circular"),
]
for col, label, value, sub in params:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("")

# ── Visualizations row ────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.55])

with col_left:
    st.markdown("## Polarization Graph")
    fig_ell = animate_polarization(E_mid)
    st.pyplot(fig_ell, use_container_width=True)
    plt.close(fig_ell)

with col_right:
    st.markdown("## Intensity vs Analyzer Angle")
    fig_int = intensity_vs_analyzer(E_in, pol_angle, use_qwp, use_hwp, analyzer_angle)
    st.pyplot(fig_int, use_container_width=True)
    plt.close(fig_int)

# ── Stokes / Poincaré ─────────────────────────────────────────────────────────
st.markdown("## Stokes Parameters & Poincaré Projection")
fig_stk = stokes_sphere_projection(stokes)
st.pyplot(fig_stk, use_container_width=True)
plt.close(fig_stk)

# ── Physics Formulas inline ───────────────────────────────────────────────────
with st.expander("📐 Jones Calculus Cheat-Sheet", expanded=False):
    st.markdown("""
    **Jones vector** — 2-element complex vector describing the amplitude and phase of Ex, Ey:

    <div class="formula">E = [Ex, Ey]ᵀ  where  Ex = A·e^(iδ)</div>

    **Polarizer matrix** (angle θ):

    <div class="formula">M_pol = [[cos²θ, cosθ·sinθ], [cosθ·sinθ, sin²θ]]</div>

    **Wave plate** (retardation Γ, fast axis α):

    <div class="formula">M_wp = R(-α) · diag(e^(-iΓ/2), e^(+iΓ/2)) · R(α)</div>

    **Malus' Law**:

    <div class="formula">I = I₀ · cos²(θ_analyzer − θ_polarizer)</div>

    **Stokes Parameters**:

    <div class="formula">S0 = |Ex|²+|Ey|²  S1 = |Ex|²-|Ey|²  S2 = 2Re(Ex·Ey*)  S3 = 2Im(Ex·Ey*)</div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HARDWARE MAPPING SECTION
# ─────────────────────────────────────────────────────────────────────────────
if mode == 'Hardware + Malus Law':
    st.markdown("---")
    st.markdown("## 🔧 Hardware Mapping")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<table class="hw-table">'
                    '<tr><th>Simulation</th><th>Hardware Component</th><th>Role</th></tr>'
                    '<tr><td>Jones Vector</td><td>Laser source</td><td>Coherent light beam</td></tr>'
                    '<tr><td>Polarizer Matrix</td><td>Linear polarizer</td><td>Selects E-field axis</td></tr>'
                    '<tr><td>QWP Matrix (Γ=π/2)</td><td>Quarter-wave plate</td><td>Linear → Circular</td></tr>'
                    '<tr><td>HWP Matrix (Γ=π)</td><td>Half-wave plate</td><td>Rotates polarization 2α</td></tr>'
                    '<tr><td>Analyzer Matrix</td><td>Rotating polarizer</td><td>Projection / detection</td></tr>'
                    '<tr><td>I = |E_out|²</td><td>Photodetector / ADC</td><td>Voltage ∝ Intensity</td></tr>'
                    '<tr><td>Stokes S3</td><td>Waveplate + PBS</td><td>Measure circularity</td></tr>'
                    '</table>', unsafe_allow_html=True)

    with col_b:
        st.markdown("**Predicted hardware behaviour:**")

        # Malus law sweep
        angles_hw = np.linspace(0, 360, 720)
        curves = {}
        for label, qwp, hwp in [
            ('No waveplates (cos²)',  False, False),
            ('With QWP (constant)',   True,  False),
            ('With HWP (2× shift)',   False, True),
        ]:
            c_vals = []
            for a in angles_hw:
                _, I_val = compute_output(E_in, pol_angle, qwp, hwp, a, qwp_axis, hwp_axis)
                c_vals.append(I_val)
            curves[label] = c_vals

        fig_hw2, ax_hw = plt.subplots(figsize=(6, 3))
        _fig_style(fig_hw2, ax_hw)
        palette = [ACCENT, ACCENT2, ACCENT3]
        for (lbl, vals), col in zip(curves.items(), palette):
            ax_hw.plot(angles_hw, vals, lw=1.8, label=lbl, color=col)
        ax_hw.set_xlabel('Analyzer Angle (°)', fontsize=8)
        ax_hw.set_ylabel('Intensity', fontsize=8)
        ax_hw.set_title('Malus Law — All Modes', fontsize=9, pad=6)
        ax_hw.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
        ax_hw.set_xlim(0, 360)
        fig_hw2.tight_layout(pad=0.8)
        st.pyplot(fig_hw2, use_container_width=True)
        plt.close(fig_hw2)

        st.markdown("""
        <div class="info-box">
        <b>QWP</b> converts linear → circular → nearly uniform intensity<br>
        <b>HWP</b> rotates polarization axis by 2α — shifts the cos² curve<br>
        <b>No plate</b> → classic Malus' Law: I = I₀ cos²(θ)
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p style="color:#1e3a5f;font-size:0.72rem;text-align:center;margin-top:30px">'
            'Polarization Optics Visual Lab · Jones Calculus Engine · '
            'Built with Streamlit + NumPy + Matplotlib</p>',
            unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  DRIVER.JS OVERLAY TOUR  ░░
# ─────────────────────────────────────────────────────────────────────────────
driver_js_code = """
<script>
    const parentWindow = window.parent;
    const parentDoc = parentWindow.document;

    function getTargetElement(text, isGraph) {
        const headers = Array.from(parentDoc.querySelectorAll('h1, h2, h3, h4, h5, h6, .info-box'));
        const target = headers.find(h => h.textContent.toUpperCase().includes(text.toUpperCase()));
        if (target) {
            if (target.classList.contains('info-box')) return target;
            const container = target.closest('[data-testid="stElementContainer"]');
            if (isGraph && container && container.nextElementSibling) {
                return container.nextElementSibling;
            }
            return container ? container : target;
        }
        return null;
    }

    function initTour() {
        if (!parentWindow.driver) return;
        const driverObj = parentWindow.driver.js.driver;
        const tour = driverObj({
            showProgress: true,
            animate: true,
            allowClose: false,
            doneBtnText: 'Finish ✅',
            nextBtnText: 'Next ➡️',
            prevBtnText: '⬅️ Previous',
            steps: [
                {
                    element: getTargetElement('Pipeline', false),
                    popover: { title: '1. Optical Components Overview', description: "The pipeline includes a Laser, Polarizer, Waveplates (Quarter/Half), an Analyzer, and a Sensor. These elements manipulate the electromagnetic wave's phase and amplitude.", side: 'bottom', align: 'start' }
                },
                {
                    element: getTargetElement('Mode', false),
                    popover: { title: '2. Controls: Mode', description: "Choose between Simulation or Hardware mapping modes in the sidebar. This dictates whether you see theoretical ellipses or real expected hardware behavior.", side: 'right', align: 'start' }
                },
                {
                    element: getTargetElement('Input Light', false),
                    popover: { title: '3. Controls: Input Light', description: "Select the initial polarization state from linear, circular, or elliptical options. You can also precisely adjust the phase offset for the elliptical light state.", side: 'right', align: 'start' }
                },
                {
                    element: getTargetElement('Optical Components', false),
                    popover: { title: '4. Controls: Optical Components', description: "Adjust angles for the Polarizer and Analyzer to control light transmission dynamically. Toggle QWP/HWP to convert linear light to circular, or to rotate the polarization axis.", side: 'right', align: 'start' }
                },
                {
                    element: getTargetElement('Hardware Pipeline — Live Wave Animation', true),
                    popover: { title: '5. Graph 1: Live Wave Animation', description: "An animated HTML canvas tracking the real-time electromagnetic wave behavior. It displays the Ex and Ey components propagating through each physical optical element.", side: 'bottom', align: 'center' }
                },
                {
                    element: getTargetElement('Polarization Ellipse', true),
                    popover: { title: '6. Graph 2: Polarization Ellipse', description: "Traces the Ex versus Ey components over one full continuous wave cycle. The moving dot shows the tip of the E-field vector, forming the actual polarization shape.", side: 'bottom', align: 'center' }
                },
                {
                    element: getTargetElement('Intensity vs Analyzer', true),
                    popover: { title: '7. Graph 3: Intensity vs Analyzer Angle', description: "Visualizes the transmitted light's intensity as the analyzer is rotated from 0 to 360 degrees. The dashed line represents the theoretical intensity limit according to Malus' law.", side: 'bottom', align: 'center' }
                },
                {
                    element: getTargetElement('Stokes Parameters & Poincaré', true),
                    popover: { title: '8. Graph 4: Stokes Parameters & Poincaré Sphere', description: "Displays the normalized Stokes parameters (s1, s2, s3) in a bar chart. The adjacent circle projects the current optical state onto the S1-S2 plane of the Poincaré sphere.", side: 'bottom', align: 'center' }
                }
            ],
            onDestroyed: () => {
                parentWindow.localStorage.setItem("tour_done", "true");
            }
        });
        
        const checkReady = setInterval(() => {
            if (getTargetElement('Pipeline', false) && getTargetElement('Mode', false)) {
                clearInterval(checkReady);
                setTimeout(() => { tour.drive(); }, 300);
            }
        }, 200);
        setTimeout(() => clearInterval(checkReady), 10000);
    }

    if (!parentWindow.localStorage.getItem("tour_done")) {
        if (!parentDoc.getElementById('driver-css')) {
            const link = parentDoc.createElement('link');
            link.id = 'driver-css';
            link.rel = 'stylesheet';
            link.href = 'https://cdn.jsdelivr.net/npm/driver.js@1.0.1/dist/driver.css';
            parentDoc.head.appendChild(link);
        }
        if (!parentDoc.getElementById('driver-js')) {
            const script = parentDoc.createElement('script');
            script.id = 'driver-js';
            script.src = 'https://cdn.jsdelivr.net/npm/driver.js@1.0.1/dist/driver.js.iife.js';
            script.onload = () => { setTimeout(initTour, 100); };
            parentDoc.head.appendChild(script);
        } else {
            initTour();
        }
    }
</script>
"""
components.html(driver_js_code, height=0, width=0)