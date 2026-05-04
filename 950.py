# ═══════════════════════════════════════════════════════════════════
#  VXSIA UNIFIED ANALYTICS DASHBOARD
#  Sosial İnnovasiya Modeli + Regional ASAN Data + Proaktiv KPI
#  Solow Böyümə Çərçivəsi × VXSIA Layihəsi Sintezi
#  IBM Plex Mono — Dark Analytics Theme
# ═══════════════════════════════════════════════════════════════════

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  SƏHIFƏ KONFİQURASİYASI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VXSIA Analitik Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — IBM Plex + Tünd Mavi Tema
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp {
    background: linear-gradient(160deg, #0a0f1e 0%, #0d1117 60%, #0a1628 100%);
    color: #e6edf3;
}
h1, h2, h3, h4 {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #58a6ff !important;
}
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
[data-testid="stSidebar"] * { color: #c9d9f0 !important; }
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; color: #58a6ff; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 6px 0 4px 0; border-bottom: 1px solid #21262d; margin-bottom: 10px;
}
.hero-block {
    background: linear-gradient(90deg, #0d1f3e 0%, #0d1117 60%);
    border: 1px solid #1e3a6e; border-radius: 12px;
    padding: 26px 36px; margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.hero-block::after {
    content: ''; position: absolute; right: -60px; top: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(88,166,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'IBM Plex Mono', monospace; font-size: 1.9rem;
    font-weight: 700; color: #ffffff !important; margin: 0 0 6px 0; letter-spacing: -0.5px;
}
.hero-sub {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;
    color: #58a6ff; margin: 0; letter-spacing: 0.5px;
}
.hero-badge {
    display: inline-block; background: rgba(88,166,255,0.1);
    border: 1px solid #2a5298; border-radius: 4px; padding: 2px 10px;
    font-size: 0.7rem; color: #58a6ff; font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;
}
.mcard {
    background: #161b22; border: 1px solid #21262d; border-radius: 10px;
    padding: 18px 20px; margin-bottom: 8px; position: relative;
    overflow: hidden; transition: border-color 0.2s;
}
.mcard:hover { border-color: #3a7bd5; }
.mcard-accent { position: absolute; top: 0; left: 0; width: 100%; height: 3px; border-radius: 10px 10px 0 0; }
.mcard-val { font-size: 1.8rem; font-weight: 700; font-family: 'IBM Plex Mono', monospace; color: #3fb950; line-height: 1.1; }
.mcard-lbl { font-size: 0.78rem; color: #6e7681; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.3px; }
.mcard-delta { font-size: 0.8rem; font-family: 'IBM Plex Mono', monospace; margin-top: 6px; font-weight: 600; }
.d-pos { color: #3fb950; } .d-neg { color: #ff7b72; } .d-neu { color: #58a6ff; }
.sec-hdr {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; font-weight: 700;
    color: #8b949e; text-transform: uppercase; letter-spacing: 2px;
    border-left: 3px solid #58a6ff; padding-left: 10px; margin: 22px 0 14px 0;
}
.stTabs [data-baseweb="tab-list"] { background: #0d1117; border-bottom: 1px solid #21262d !important; }
.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace !important; font-size: 0.78rem !important; color: #6e7681 !important; padding: 10px 18px !important; }
.stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; background: rgba(88,166,255,0.05) !important; }
[data-testid="stDataFrame"] { border: 1px solid #21262d; border-radius: 8px; }
.stSelectbox label, .stSlider label, .stNumberInput label, .stMultiSelect label {
    color: #8b949e !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.75rem !important;
}
hr { border-color: #21262d !important; }
.ibox {
    background: rgba(88,166,255,0.07); border: 1px solid rgba(88,166,255,0.25);
    border-radius: 8px; padding: 14px 18px; font-size: 0.82rem; color: #c9d9f0;
    font-family: 'IBM Plex Sans', sans-serif; line-height: 1.6; margin-bottom: 16px;
}
.warnbox {
    background: rgba(240,136,62,0.08); border: 1px solid rgba(240,136,62,0.3);
    border-radius: 8px; padding: 12px 16px; font-size: 0.8rem; color: #f0883e;
    font-family: 'IBM Plex Mono', monospace; margin-bottom: 12px;
}
.tag-green { background: rgba(63,185,80,0.12); color: #3fb950; border: 1px solid rgba(63,185,80,0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-family: 'IBM Plex Mono', monospace; }
.tag-blue  { background: rgba(88,166,255,0.12); color: #58a6ff; border: 1px solid rgba(88,166,255,0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-family: 'IBM Plex Mono', monospace; }
.tag-amber { background: rgba(240,136,62,0.12); color: #f0883e; border: 1px solid rgba(240,136,62,0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-family: 'IBM Plex Mono', monospace; }
.tag-red   { background: rgba(255,123,114,0.12); color: #ff7b72; border: 1px solid rgba(255,123,114,0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-family: 'IBM Plex Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-section">⬡ VXSIA PANEL</div>', unsafe_allow_html=True)
    st.markdown("**Sosial İnnovasiya Modeli**")
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Model Parametrləri</div>', unsafe_allow_html=True)
    s_rate       = st.slider("Sosial Xidmət İnvestisiya Faizi (s)", 0.05, 0.50, 0.25, 0.01,
                             help="Sosial xidmətlərə ayrılan büdcə payı")
    delta        = st.slider("Sistem Köhnəlmə Dərəcəsi (δ)", 0.01, 0.15, 0.05, 0.005,
                             help="Xidmət infrastrukturunun illiq deqradasiyası")
    n_pop        = st.slider("Əhali Artımı (n)", 0.005, 0.03, 0.012, 0.001)
    g_tech       = st.slider("Texnoloji İrəliləyiş (g)", 0.01, 0.05, 0.025, 0.005,
                             help="SİVA-AI effektivliyinin artım tempi")
    alpha        = st.slider("Kapital Elastikliyi (α)", 0.20, 0.60, 0.35, 0.05)
    ai_multiplier = st.slider("SİVA-AI Gücləndiricisi (x)", 1.0, 3.0, 1.5, 0.1,
                              help="AI sisteminin xidmət çatdırılmasına multiplikator təsiri")

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Regional Filterlər</div>', unsafe_allow_html=True)
    all_regions  = ["Bakı", "Abşeron", "Gəncə-Qazax", "Şirvan", "Lənkəran", "Mil-Muğan", "Aran", "Dağlıq Şirvan"]
    all_sectors  = ["Sosial Müdafiə", "Əmək Bazarı", "Səhiyyə", "Təhsil", "Rəqəmsal Xidmətlər", "Yaşlı Baxım"]
    selected_regions = st.multiselect("Regionlar", all_regions, default=all_regions[:5])
    selected_sectors = st.multiselect("Xidmət Sektorları", all_sectors, default=all_sectors)

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Monte Carlo</div>', unsafe_allow_html=True)
    mc_runs  = st.selectbox("Simulyasiya sayı", [500, 1000, 2000, 5000], index=1)
    mc_years = st.slider("Proqnoz ili", 5, 30, 15)
    seed_val = st.number_input("Toxum (seed)", value=42, step=1)

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#484f58;line-height:1.8;">
    VXSIA Dashboard v1.0<br>
    Sosial İnnovasiya Modeli<br>
    Solow (1956) × VXSIA (2026)<br>
    Azərbaycan Respublikası
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  HERO BAŞLIQ
# ═══════════════════════════════════════════════
st.markdown("""
<div class="hero-block">
  <div class="hero-badge">VXSIA · Strateji Analitika · 2026</div>
  <div class="hero-title">Vətəndaşlara Xidmət &amp; Sosial İnnovasiyalar Agentliyi</div>
  <div class="hero-sub">Proaktiv Xidmət Modeli × Solow Böyümə Çərçivəsi × Regional Kapital Analitikası</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  MODEL HESABLAMAları — SOLOW × SOSIAL
# ═══════════════════════════════════════════════
k_vals = np.linspace(0.01, 20, 500)
# Sosial kapital funksiyası: Cobb-Douglas + AI multiplier
y_vals = ai_multiplier * (k_vals ** alpha)
sf_k   = s_rate * y_vals
dep_k  = (delta + n_pop + g_tech) * k_vals

# Tarazlıq nöqtəsi (Sosial Sabit Vəziyyət)
k_star_idx = np.argmin(np.abs(sf_k - dep_k))
k_star = k_vals[k_star_idx]
y_star = ai_multiplier * (k_star ** alpha)

# Effektiv xidmət kapitalı
c_star   = (1 - s_rate) * y_star
welfare_index = y_star * (1 + 0.15 * (ai_multiplier - 1))

# ─────────────────────────────────────────────
#  YUXARI METRİK KARTLAR
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("#58a6ff", f"{k_star:.3f}", "Sosial k* (Sabit Vəziyyət)", f"s={s_rate:.0%}  δ={delta:.3f}", "d-neu"),
    ("#3fb950", f"{y_star:.3f}", "Xidmət Çıxışı y* (per kapita)", f"AI×{ai_multiplier:.1f}  α={alpha:.2f}", "d-pos"),
    ("#f0883e", f"{c_star:.3f}", "Effektiv İstehlak c*", f"(1−s)·y* = {1-s_rate:.0%}×y*", "d-neu"),
    ("#bc8cff", f"{welfare_index:.3f}", "Refah İndeksi", f"AI multiplikator təsiri", "d-pos"),
    ("#ffd700", f"{ai_multiplier:.1f}×", "SİVA-AI Gücləndirici", "Proaktiv xidmət faktoru", "d-neu"),
]
for col, (accent, val, lbl, delta_txt, cls) in zip([c1,c2,c3,c4,c5], metrics):
    with col:
        st.markdown(f"""
        <div class="mcard">
          <div class="mcard-accent" style="background:{accent};"></div>
          <div class="mcard-val" style="color:{accent};">{val}</div>
          <div class="mcard-lbl">{lbl}</div>
          <div class="mcard-delta {cls}">{delta_txt}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  TABLAR
# ═══════════════════════════════════════════════
tabs = st.tabs([
    "⬡ Sosial Model",
    "📍 Regional ASAN Analizi",
    "🎲 Monte Carlo Simulyasiyası",
    "📈 Makro KPI Zaman Seriyası",
    "🔗 Kross Analiz",
    "🤖 SİVA-AI Proqnoz",
])

# ╔══════════════════════════════════════════════╗
# ║  TAB 1 — SOSİAL BÖYÜMƏ MODELİ               ║
# ╚══════════════════════════════════════════════╝
with tabs[0]:
    st.markdown('<div class="sec-hdr">Sosial Kapital Böyümə Modeli — Solow × VXSIA Çərçivəsi</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ibox">
    <b>Sosial Sabit Vəziyyət:</b> k* = <b>{k_star:.4f}</b> &nbsp;|&nbsp;
    y* = <b>{y_star:.4f}</b> &nbsp;|&nbsp; c* = <b>{c_star:.4f}</b><br>
    Modeldə sosial xidmət kapitalı Cobb-Douglas funksiyası əsasında modelləşdirilir.
    SİVA-AI multiplikatoru (<b>×{ai_multiplier:.1f}</b>) proaktiv xidmətin ənənəvi sistemə nisbət
    əlavə effektivliyini əks etdirir. Sabit vəziyyətdə <b>s·y* = (δ+n+g)·k*</b> tarazlığı ödənir.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=k_vals, y=sf_k, name=f"Xidmət investisiyası s·f(k) [s={s_rate:.0%}]",
                                  line=dict(color="#58a6ff", width=2.5)))
        fig1.add_trace(go.Scatter(x=k_vals, y=dep_k, name=f"Köhnəlmə (δ+n+g)·k [{delta+n_pop+g_tech:.3f}]",
                                  line=dict(color="#ff7b72", width=2.5, dash="dash")))
        fig1.add_trace(go.Scatter(x=k_vals, y=y_vals, name=f"f(k) = {ai_multiplier:.1f}·k^{alpha}",
                                  line=dict(color="#3fb950", width=1.5, dash="dot")))
        fig1.add_trace(go.Scatter(x=[k_star], y=[sf_k[k_star_idx]],
                                  mode='markers', name=f"k* = {k_star:.3f}",
                                  marker=dict(color="#ffd700", size=14, symbol="star",
                                              line=dict(color="white", width=1.5))))
        fig1.add_vline(x=k_star, line_dash="dot", line_color="#ffd700", opacity=0.5,
                       annotation_text=f"k*={k_star:.3f}", annotation_font_color="#ffd700",
                       annotation_font_family="IBM Plex Mono")
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title="Sosial Kapital İntensivliyi (k)"),
            yaxis=dict(gridcolor="#21262d", title="Çıxış / İnvestisiya"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=10)),
            height=380, margin=dict(t=10, b=20),
            title=dict(text="Sosial Kapital — Sabit Vəziyyət Analizi", font=dict(color="#58a6ff", size=13))
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Kapital dinamikası simulyasiyası
        T = 60
        k_t = [0.5]
        for _ in range(T - 1):
            dk = s_rate * ai_multiplier * (k_t[-1] ** alpha) - (delta + n_pop + g_tech) * k_t[-1]
            k_t.append(max(k_t[-1] + 0.05 * dk, 0.001))
        y_t = [ai_multiplier * k ** alpha for k in k_t]
        c_t = [(1 - s_rate) * y for y in y_t]

        fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             vertical_spacing=0.08,
                             subplot_titles=["k(t) — Kapital dinamikası", "y(t), c(t) — Çıxış & İstehlak"])
        fig2.add_trace(go.Scatter(x=list(range(T)), y=k_t, line=dict(color="#58a6ff", width=2.5),
                                  name="k(t)"), row=1, col=1)
        fig2.add_hline(y=k_star, line_dash="dot", line_color="#ffd700", opacity=0.6,
                       annotation_text="k*", row=1, col=1)
        fig2.add_trace(go.Scatter(x=list(range(T)), y=y_t, line=dict(color="#3fb950", width=2),
                                  name="y(t)"), row=2, col=1)
        fig2.add_trace(go.Scatter(x=list(range(T)), y=c_t, line=dict(color="#f0883e", width=2),
                                  fill="tozeroy", fillcolor="rgba(240,136,62,0.08)", name="c(t)"), row=2, col=1)
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e", size=10),
            xaxis2=dict(gridcolor="#21262d", title="İl"), xaxis=dict(gridcolor="#21262d"),
            yaxis=dict(gridcolor="#21262d"), yaxis2=dict(gridcolor="#21262d"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=10)),
            height=380, margin=dict(t=30, b=10),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # AI effekti müqayisəsi
    st.markdown('<div class="sec-hdr">SİVA-AI Multiplikatorunun Sabit Vəziyyətə Təsiri</div>', unsafe_allow_html=True)
    ai_range  = np.linspace(1.0, 3.0, 50)
    k_stars_ai, y_stars_ai, c_stars_ai = [], [], []
    for ai_m in ai_range:
        y_v = ai_m * (k_vals ** alpha)
        sf  = s_rate * y_v
        idx = np.argmin(np.abs(sf - dep_k))
        ks  = k_vals[idx]; ys = ai_m * ks ** alpha
        k_stars_ai.append(ks); y_stars_ai.append(ys); c_stars_ai.append((1 - s_rate) * ys)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=ai_range, y=k_stars_ai, name="k* (sabit vəz.)", line=dict(color="#58a6ff", width=2)))
    fig3.add_trace(go.Scatter(x=ai_range, y=y_stars_ai, name="y* (çıxış)", line=dict(color="#3fb950", width=2)))
    fig3.add_trace(go.Scatter(x=ai_range, y=c_stars_ai, name="c* (istehlak)", line=dict(color="#f0883e", width=2)))
    fig3.add_vline(x=ai_multiplier, line_dash="dot", line_color="#ffd700",
                   annotation_text=f"Cari AI×{ai_multiplier:.1f}", annotation_font_color="#ffd700",
                   annotation_font_family="IBM Plex Mono")
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
        font=dict(family="IBM Plex Mono", color="#8b949e"),
        xaxis=dict(gridcolor="#21262d", title="SİVA-AI Multiplikatoru"),
        yaxis=dict(gridcolor="#21262d", title="Sabit Vəziyyət Dəyəri"),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=10)),
        height=280, margin=dict(t=10, b=20),
    )
    st.plotly_chart(fig3, use_container_width=True)


# ╔══════════════════════════════════════════════╗
# ║  TAB 2 — REGİONAL ASAN ANALİZİ              ║
# ╚══════════════════════════════════════════════╝
with tabs[1]:
    st.markdown('<div class="sec-hdr">Regional ASAN Xidmət Analizi — Müraciət & İnvestisiya Data</div>', unsafe_allow_html=True)

    # Sintetik regional data
    np.random.seed(42)
    regions_data = []
    region_profiles = {
        "Bakı":             dict(base_inv=420, base_app=85000, base_udm=6.2, base_ixr=310),
        "Abşeron":          dict(base_inv=185, base_app=32000, base_udm=4.8, base_ixr=120),
        "Gəncə-Qazax":     dict(base_inv=210, base_app=28000, base_udm=5.1, base_ixr=95),
        "Şirvan":           dict(base_inv=140, base_app=18000, base_udm=4.2, base_ixr=65),
        "Lənkəran":         dict(base_inv=120, base_app=22000, base_udm=3.9, base_ixr=45),
        "Mil-Muğan":        dict(base_inv=95,  base_app=14000, base_udm=3.5, base_ixr=38),
        "Aran":             dict(base_inv=105, base_app=16000, base_udm=3.8, base_ixr=42),
        "Dağlıq Şirvan":   dict(base_inv=75,  base_app=9500,  base_udm=3.2, base_ixr=28),
    }
    sectors_profiles = {
        "Sosial Müdafiə":      dict(mult_inv=1.4, mult_job=1.2),
        "Əmək Bazarı":         dict(mult_inv=1.1, mult_job=1.8),
        "Səhiyyə":             dict(mult_inv=1.3, mult_job=1.3),
        "Təhsil":              dict(mult_inv=1.2, mult_job=1.5),
        "Rəqəmsal Xidmətlər": dict(mult_inv=1.6, mult_job=1.1),
        "Yaşlı Baxım":         dict(mult_inv=0.9, mult_job=1.4),
    }
    for region in all_regions:
        p = region_profiles[region]
        for sektor in all_sectors:
            sp = sectors_profiles[sektor]
            inv   = p["base_inv"] * sp["mult_inv"] * np.random.uniform(0.85, 1.15)
            jobs  = int(inv * 12 * sp["mult_job"] * np.random.uniform(0.9, 1.1))
            apps  = int(p["base_app"] * np.random.uniform(0.8, 1.2))
            proaktiv_pct = np.random.uniform(12, 52)
            udm   = p["base_udm"] * np.random.uniform(0.9, 1.1)
            ixr   = p["base_ixr"] * sp["mult_inv"] * np.random.uniform(0.8, 1.2)
            sat   = np.random.uniform(72, 94)
            regions_data.append({
                "Region": region, "Sektor": sektor,
                "İnvestisiya (mln AZN)": round(inv, 1),
                "Yeni İş Yerləri": jobs,
                "Müraciət Sayı": apps,
                "Proaktiv Faiz (%)": round(proaktiv_pct, 1),
                "ÜDM Artımı (%)": round(udm, 2),
                "İxracat (mln AZN)": round(ixr, 1),
                "Məmnunluq (%)": round(sat, 1),
            })
    df_reg = pd.DataFrame(regions_data)
    df_filt = df_reg[df_reg["Region"].isin(selected_regions) & df_reg["Sektor"].isin(selected_sectors)]

    if df_filt.empty:
        st.markdown('<div class="warnbox">⚠ Heç bir region/sektor seçilməyib. Soldakı filteri yenilə.</div>', unsafe_allow_html=True)
    else:
        # Aggregasiya
        reg_agg = df_filt.groupby("Region").agg(
            İnvestisiya=("İnvestisiya (mln AZN)", "sum"),
            İş_Yerləri=("Yeni İş Yerləri", "sum"),
            Müraciət=("Müraciət Sayı", "sum"),
            Proaktiv=("Proaktiv Faiz (%)", "mean"),
            ÜDM=("ÜDM Artımı (%)", "mean"),
            İxracat=("İxracat (mln AZN)", "sum"),
            Məmnunluq=("Məmnunluq (%)", "mean"),
        ).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=reg_agg["Region"], y=reg_agg["İnvestisiya"],
                marker=dict(color=reg_agg["ÜDM"], colorscale="Blues", showscale=True,
                            colorbar=dict(title=dict(text="ÜDM %", font=dict(color="#8b949e")),
                                          tickfont=dict(color="#8b949e"), outlinewidth=0)),
                text=reg_agg["İnvestisiya"].round(0), textposition="outside",
                textfont=dict(family="IBM Plex Mono", size=10, color="#c9d9f0"),
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Mono", color="#8b949e"),
                xaxis=dict(gridcolor="#21262d"), yaxis=dict(gridcolor="#21262d", title="mln AZN"),
                title=dict(text="Regional İnvestisiya (ÜDM ilə rənglənmiş)", font=dict(color="#58a6ff", size=12)),
                height=340, margin=dict(t=40, b=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            # Müraciət vs Proaktiv faiz scatter
            fig_sc = go.Figure()
            colors_sc = ['#58a6ff','#3fb950','#f0883e','#ffd700','#bc8cff','#ff7b72','#56d364','#e3b341']
            for i, row in reg_agg.iterrows():
                fig_sc.add_trace(go.Scatter(
                    x=[row["Proaktiv"]], y=[row["Məmnunluq"]],
                    mode="markers+text", name=row["Region"],
                    marker=dict(size=max(14, row["İnvestisiya"] / 40),
                                color=colors_sc[i % len(colors_sc)],
                                line=dict(color="white", width=1.5), opacity=0.88),
                    text=[row["Region"]], textposition="top center",
                    textfont=dict(family="IBM Plex Mono", size=9, color="#c9d9f0"),
                ))
            fig_sc.add_vline(x=45, line_dash="dot", line_color="#ffd700", opacity=0.5,
                             annotation_text="KPI Hədəf: 45%", annotation_font_color="#ffd700",
                             annotation_font_family="IBM Plex Mono")
            fig_sc.add_hline(y=85, line_dash="dot", line_color="#3fb950", opacity=0.5,
                             annotation_text="Məmn. hədəfi: 85%", annotation_font_color="#3fb950",
                             annotation_font_family="IBM Plex Mono")
            fig_sc.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Mono", color="#8b949e"),
                xaxis=dict(gridcolor="#21262d", title="Proaktiv Xidmət Faizi (%)"),
                yaxis=dict(gridcolor="#21262d", title="Vətəndaş Məmnunluğu (%)"),
                title=dict(text="Proaktiv Faiz vs Məmnunluq (ölçü = İnvestisiya)", font=dict(color="#58a6ff", size=12)),
                showlegend=False, height=340, margin=dict(t=40, b=10),
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        # Sektor treemap
        sec_agg = df_filt.groupby("Sektor").agg(
            İnvestisiya=("İnvestisiya (mln AZN)", "sum"),
            Müraciət=("Müraciət Sayı", "sum"),
            Proaktiv=("Proaktiv Faiz (%)", "mean"),
        ).reset_index()

        c3, c4 = st.columns(2)
        with c3:
            fig_tm = px.treemap(sec_agg, path=["Sektor"], values="İnvestisiya",
                                color="Proaktiv", color_continuous_scale="Blues",
                                title="Sektor Treemap — İnvestisiya (Proaktiv % ilə)")
            fig_tm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Mono", color="#c9d9f0"),
                title_font=dict(color="#58a6ff", size=12),
                height=300, margin=dict(t=40, b=10),
            )
            st.plotly_chart(fig_tm, use_container_width=True)

        with c4:
            # Sektor müqayisə radar
            sec_norm = sec_agg.copy()
            for col in ["İnvestisiya", "Müraciət", "Proaktiv"]:
                mn, mx = sec_norm[col].min(), sec_norm[col].max()
                sec_norm[col] = (sec_norm[col] - mn) / (mx - mn + 1e-9) * 100

            fig_rad = go.Figure()
            for i, row in sec_norm.iterrows():
                fig_rad.add_trace(go.Scatterpolar(
                    r=[row["İnvestisiya"], row["Müraciət"], row["Proaktiv"],
                       row["İnvestisiya"]],
                    theta=["İnvestisiya", "Müraciət", "Proaktiv", "İnvestisiya"],
                    fill="toself", fillcolor=f"rgba({50+i*30},{100+i*20},{200-i*20},0.12)",
                    line=dict(color=colors_sc[i % len(colors_sc)], width=1.8),
                    name=row["Sektor"],
                ))
            fig_rad.update_layout(
                polar=dict(bgcolor="#161b22",
                           radialaxis=dict(gridcolor="#21262d", tickfont=dict(color="#6e7681", size=8)),
                           angularaxis=dict(gridcolor="#21262d", tickfont=dict(color="#c9d9f0", size=10))),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Mono", color="#8b949e"),
                legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=9)),
                title=dict(text="Sektor Radar (Normlaşdırılmış)", font=dict(color="#58a6ff", size=12)),
                height=300, margin=dict(t=40, b=10),
            )
            st.plotly_chart(fig_rad, use_container_width=True)

        # Data cədvəli
        st.markdown("**Regional Tam Data Cədvəli**")
        st.dataframe(
            reg_agg.style
                .background_gradient(subset=["İnvestisiya"], cmap="Blues")
                .background_gradient(subset=["Proaktiv"], cmap="Greens")
                .background_gradient(subset=["Məmnunluq"], cmap="Oranges")
                .format({"İnvestisiya": "{:.1f}", "Proaktiv": "{:.1f}%",
                         "ÜDM": "{:.2f}%", "Məmnunluq": "{:.1f}%"}),
            use_container_width=True,
        )


# ╔══════════════════════════════════════════════╗
# ║  TAB 3 — MONTE CARLO SİMULYASİYASI          ║
# ╚══════════════════════════════════════════════╝
with tabs[2]:
    st.markdown('<div class="sec-hdr">Monte Carlo — Proaktiv Xidmət Böyümə Ssenariləri</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ibox">
    <b>{mc_runs:,}</b> təsadüfi ssenaridə <b>{mc_years}</b> il ərzində proaktiv xidmət kapitalının
    inkişaf ehtimalı modelləşdirilir. Parametr qeyri-müəyyənliyi: investisiya faizi ±15%,
    texnoloji irəliləyiş ±20%, SİVA-AI multiplikatoru ±10% standart sapma ilə simulasiya edilir.
    </div>
    """, unsafe_allow_html=True)

    np.random.seed(int(seed_val))
    years = np.arange(mc_years + 1)
    mc_paths, mc_final, mc_welfare = [], [], []

    for _ in range(mc_runs):
        s_r  = np.clip(np.random.normal(s_rate, s_rate * 0.15), 0.05, 0.55)
        d_r  = np.clip(np.random.normal(delta, delta * 0.10), 0.01, 0.20)
        n_r  = np.clip(np.random.normal(n_pop, n_pop * 0.10), 0.001, 0.05)
        g_r  = np.clip(np.random.normal(g_tech, g_tech * 0.20), 0.005, 0.08)
        ai_r = np.clip(np.random.normal(ai_multiplier, ai_multiplier * 0.10), 1.0, 4.0)
        al_r = np.clip(np.random.normal(alpha, 0.04), 0.15, 0.65)

        path = [0.5]
        for _ in range(mc_years):
            shock = np.random.normal(1.0, 0.04)
            dk = s_r * ai_r * shock * (path[-1] ** al_r) - (d_r + n_r + g_r) * path[-1]
            path.append(max(path[-1] + 0.05 * dk, 0.001))
        mc_paths.append(path)
        mc_final.append(path[-1])
        mc_welfare.append(ai_r * path[-1] ** al_r * (1 - s_r))

    mc_arr = np.array(mc_paths)
    p5  = np.percentile(mc_arr, 5, axis=0)
    p25 = np.percentile(mc_arr, 25, axis=0)
    p50 = np.percentile(mc_arr, 50, axis=0)
    p75 = np.percentile(mc_arr, 75, axis=0)
    p95 = np.percentile(mc_arr, 95, axis=0)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig_mc = go.Figure()
        # Şəffaf band — 5/95
        fig_mc.add_trace(go.Scatter(x=years, y=p95, fill=None, mode="lines",
                                    line=dict(color="rgba(88,166,255,0)"), showlegend=False))
        fig_mc.add_trace(go.Scatter(x=years, y=p5, fill="tonexty", mode="lines",
                                    line=dict(color="rgba(88,166,255,0)"),
                                    fillcolor="rgba(88,166,255,0.07)", name="90% Ehtimal Zonası"))
        fig_mc.add_trace(go.Scatter(x=years, y=p75, fill=None, mode="lines",
                                    line=dict(color="rgba(63,185,80,0)"), showlegend=False))
        fig_mc.add_trace(go.Scatter(x=years, y=p25, fill="tonexty", mode="lines",
                                    line=dict(color="rgba(63,185,80,0)"),
                                    fillcolor="rgba(63,185,80,0.12)", name="50% Ehtimal Zonası"))
        fig_mc.add_trace(go.Scatter(x=years, y=p50, mode="lines", name="Median (p50)",
                                    line=dict(color="#58a6ff", width=2.5)))
        fig_mc.add_trace(go.Scatter(x=years, y=p95, mode="lines", name="p95 (Optimist)",
                                    line=dict(color="#3fb950", width=1.5, dash="dot")))
        fig_mc.add_trace(go.Scatter(x=years, y=p5, mode="lines", name="p5 (Pessimist)",
                                    line=dict(color="#ff7b72", width=1.5, dash="dot")))
        fig_mc.add_hline(y=k_star, line_dash="dash", line_color="#ffd700", opacity=0.6,
                         annotation_text=f"Deterministik k*={k_star:.3f}",
                         annotation_font_color="#ffd700", annotation_font_family="IBM Plex Mono")
        fig_mc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title="İl"),
            yaxis=dict(gridcolor="#21262d", title="Sosial Kapital k(t)"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=10)),
            title=dict(text=f"Monte Carlo — {mc_runs:,} ssenaridə k(t) yayılması",
                       font=dict(color="#58a6ff", size=13)),
            height=400, margin=dict(t=40, b=20),
        )
        st.plotly_chart(fig_mc, use_container_width=True)

    with col2:
        # Final dağılım histoqramı
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=mc_final, nbinsx=50, name="k(T) dağılımı",
            marker=dict(color="#58a6ff", opacity=0.75, line=dict(color="#21262d", width=0.5)),
        ))
        fig_hist.add_vline(x=np.median(mc_final), line_dash="dash", line_color="#ffd700",
                           annotation_text=f"Median={np.median(mc_final):.3f}",
                           annotation_font_color="#ffd700", annotation_font_family="IBM Plex Mono")
        fig_hist.add_vline(x=k_star, line_dash="dot", line_color="#3fb950", opacity=0.8,
                           annotation_text=f"k*={k_star:.3f}",
                           annotation_font_color="#3fb950", annotation_font_family="IBM Plex Mono")
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title=f"k({mc_years} il)"),
            yaxis=dict(gridcolor="#21262d", title="Tezlik"),
            title=dict(text="Son İl Kapital Dağılımı", font=dict(color="#58a6ff", size=12)),
            showlegend=False, height=200, margin=dict(t=40, b=10),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # Refah dağılımı
        fig_welf = go.Figure()
        fig_welf.add_trace(go.Histogram(
            x=mc_welfare, nbinsx=50, name="Refah dağılımı",
            marker=dict(color="#3fb950", opacity=0.75, line=dict(color="#21262d", width=0.5)),
        ))
        fig_welf.add_vline(x=np.median(mc_welfare), line_dash="dash", line_color="#ffd700",
                           annotation_text=f"Med={np.median(mc_welfare):.3f}",
                           annotation_font_color="#ffd700", annotation_font_family="IBM Plex Mono")
        fig_welf.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title="c* = (1−s)·y*"),
            yaxis=dict(gridcolor="#21262d", title="Tezlik"),
            title=dict(text="Refah İndeksi Dağılımı", font=dict(color="#58a6ff", size=12)),
            showlegend=False, height=175, margin=dict(t=40, b=10),
        )
        st.plotly_chart(fig_welf, use_container_width=True)

    # MC Statistik Cədvəl
    st.markdown("**Monte Carlo Statistik Xülasəsi**")
    mc_stats = pd.DataFrame({
        "Göstərici": ["Median k(T)", "Ortalama k(T)", "Std. Sapma", "p5", "p25", "p75", "p95",
                      "Median Refah", "P(k(T) > k*)", "P(k(T) > 1.2·k*)"],
        "Dəyər": [
            f"{np.median(mc_final):.4f}", f"{np.mean(mc_final):.4f}",
            f"{np.std(mc_final):.4f}", f"{np.percentile(mc_final, 5):.4f}",
            f"{np.percentile(mc_final, 25):.4f}", f"{np.percentile(mc_final, 75):.4f}",
            f"{np.percentile(mc_final, 95):.4f}", f"{np.median(mc_welfare):.4f}",
            f"{np.mean(np.array(mc_final) > k_star)*100:.1f}%",
            f"{np.mean(np.array(mc_final) > 1.2 * k_star)*100:.1f}%",
        ],
        "Şərh": [
            "50% ssenarinin nəticəsi", "Gözlənilən dəyər", "Qeyri-müəyyənlik ölçüsü",
            "Ən pessimist 5%", "Alt kvartil", "Üst kvartil", "Ən optimist 5%",
            "Gözlənilən istehlak", "Sabit vəziyyəti keçmə ehtimalı", "20% üstəgəl keçmə ehtimalı",
        ]
    })
    st.dataframe(mc_stats.style.applymap(
        lambda v: "color:#3fb950;" if "%" in str(v) and float(v.rstrip('%')) > 50 else
                  ("color:#ff7b72;" if "%" in str(v) and float(v.rstrip('%')) < 30 else ""),
        subset=["Dəyər"]
    ), use_container_width=True, hide_index=True)


# ╔══════════════════════════════════════════════╗
# ║  TAB 4 — MAKRO KPI ZAMAN SERİYASI           ║
# ╚══════════════════════════════════════════════╝
with tabs[3]:
    st.markdown('<div class="sec-hdr">VXSIA Makro KPI — Zaman Seriyası (2020–2026 Faktiki + Proqnoz)</div>', unsafe_allow_html=True)

    years_ts = list(range(2020, 2030))
    np.random.seed(7)
    df_macro = pd.DataFrame({
        "İl": years_ts,
        "Proaktiv Faiz (%)": [3.1, 5.4, 8.2, 12.7, 19.3, 28.5, 38.1, 47.2, 55.8, 62.4],
        "Vətəndaş Məmnunluğu (%)": [68, 70, 71, 73, 76, 80, 84, 87, 89, 91],
        "ASAN Müraciət (min)": [890, 920, 950, 1020, 1100, 1180, 1240, 1310, 1380, 1450],
        "Avtomatik Xidmət Sayı": [8, 14, 22, 35, 52, 78, 102, 118, 128, 135],
        "Orta Cavab (saat)": [72, 58, 44, 32, 21, 14, 8, 5, 3, 2],
        "Büdcə Səmərəliliyi (%)": [61, 64, 67, 71, 75, 79, 83, 86, 88, 90],
        "İş Yeri Kəsiyi (K)": [0, 2.1, 5.4, 10.2, 18.7, 31.2, 45.8, 58.3, 67.1, 73.5],
    })
    faktiki_cutoff = 2026
    df_fakt  = df_macro[df_macro["İl"] <= faktiki_cutoff]
    df_prog  = df_macro[df_macro["İl"] >= faktiki_cutoff]

    fig_macro = make_subplots(
        rows=2, cols=3, shared_xaxes=False,
        subplot_titles=["Proaktiv Xidmət Faizi (%)", "Vətəndaş Məmnunluğu (%)",
                        "Orta Cavab Müddəti (saat)", "Avtomatik Xidmət Sayı",
                        "Büdcə Səmərəliliyi (%)", "İş Yeri Kəsiyi (Kumulyativ, K)"],
        vertical_spacing=0.15, horizontal_spacing=0.08,
    )

    kpi_traces = [
        ("Proaktiv Faiz (%)", 1, 1, "#58a6ff", 45),
        ("Vətəndaş Məmnunluğu (%)", 1, 2, "#3fb950", 85),
        ("Orta Cavab (saat)", 1, 3, "#ff7b72", 24),
        ("Avtomatik Xidmət Sayı", 2, 1, "#f0883e", 120),
        ("Büdcə Səmərəliliyi (%)", 2, 2, "#bc8cff", 85),
        ("İş Yeri Kəsiyi (K)", 2, 3, "#ffd700", None),
    ]
    for col_name, row, col, color, target in kpi_traces:
        fig_macro.add_trace(go.Scatter(
            x=df_fakt["İl"], y=df_fakt[col_name], mode="lines+markers",
            line=dict(color=color, width=2.5), marker=dict(size=6),
            fill="tozeroy", fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
            name=col_name, showlegend=False,
        ), row=row, col=col)
        fig_macro.add_trace(go.Scatter(
            x=df_prog["İl"], y=df_prog[col_name], mode="lines+markers",
            line=dict(color=color, width=1.8, dash="dot"),
            marker=dict(size=5, symbol="diamond"), name=f"{col_name} (proqnoz)", showlegend=False,
        ), row=row, col=col)
        if target:
            fig_macro.add_hline(y=target, line_dash="dot", line_color="#ffd700", opacity=0.5,
                                annotation_text=f"Hədəf: {target}", row=row, col=col,
                                annotation_font_color="#ffd700", annotation_font_family="IBM Plex Mono",
                                annotation_font_size=9)

    fig_macro.update_xaxes(gridcolor="#21262d")
    fig_macro.update_yaxes(gridcolor="#21262d")
    fig_macro.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
        font=dict(family="IBM Plex Mono", color="#8b949e"),
        height=520, margin=dict(t=50, b=20),
        annotations=[dict(font=dict(color="#8b949e", size=10, family="IBM Plex Mono"))
                      for _ in range(6)],
    )
    st.plotly_chart(fig_macro, use_container_width=True)

    st.markdown("**Tam Zaman Seriyası Cədvəli (Faktiki + Proqnoz)**")
    def style_macro(df):
        styled = df.style \
            .background_gradient(subset=["Proaktiv Faiz (%)"], cmap="Blues") \
            .background_gradient(subset=["Vətəndaş Məmnunluğu (%)"], cmap="Greens") \
            .applymap(lambda v: "color:#ff7b72;" if isinstance(v, (int,float)) and v > faktiki_cutoff else "", subset=["İl"])
        return styled
    st.dataframe(style_macro(df_macro), use_container_width=True, hide_index=True)


# ╔══════════════════════════════════════════════╗
# ║  TAB 5 — KROSS ANALİZ                       ║
# ╚══════════════════════════════════════════════╝
with tabs[4]:
    st.markdown('<div class="sec-hdr">Kross Analiz — Sosial Model × Regional VXSIA Data İnteqrasiyası</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ibox">
    Bu tab iki analitik bloğu birləşdirir: Sosial kapital böyümə modelinin çıxardığı
    <b>sabit vəziyyət göstəriciləri</b> regional ASAN/VXSIA investisiya datası ilə
    müqayisə edilir. Hansı bölgənin modelin optimal nöqtəsinə ən yaxın olduğunu
    və SİVA-AI multiplikatorunun bölgəyə görə diferensial təsirini görmək mümkündür.
    </div>
    """, unsafe_allow_html=True)

    if not df_filt.empty:
        reg_agg2 = df_filt.groupby("Region").agg(
            İnvestisiya=("İnvestisiya (mln AZN)", "sum"),
            İş_Yerləri=("Yeni İş Yerləri", "sum"),
            ÜDM=("ÜDM Artımı (%)", "mean"),
            İxracat=("İxracat (mln AZN)", "sum"),
            Proaktiv=("Proaktiv Faiz (%)", "mean"),
            Məmnunluq=("Məmnunluq (%)", "mean"),
        ).reset_index()
        reg_agg2["Kapital_İntensivliyi"] = reg_agg2["İnvestisiya"] / reg_agg2["İş_Yerləri"]
        reg_agg2["Solow_Normlaşdırma"]   = reg_agg2["Kapital_İntensivliyi"] / k_star
        reg_agg2["Sosial_Skoru"] = (reg_agg2["Proaktiv"] * 0.4 +
                                     reg_agg2["Məmnunluq"] * 0.4 +
                                     reg_agg2["ÜDM"] * 5)

        col1, col2 = st.columns(2)
        with col1:
            colors_cx = ['#58a6ff','#3fb950','#f0883e','#ffd700','#bc8cff','#ff7b72','#56d364','#e3b341']
            fig_cx1 = go.Figure()
            for i, row in reg_agg2.iterrows():
                fig_cx1.add_trace(go.Scatter(
                    x=[row["Kapital_İntensivliyi"]], y=[row["ÜDM"]],
                    mode="markers+text", name=row["Region"],
                    marker=dict(size=max(12, row["İnvestisiya"] / 45),
                                color=colors_cx[i % len(colors_cx)],
                                line=dict(color="white", width=1.5), opacity=0.85),
                    text=[row["Region"]], textposition="top center",
                    textfont=dict(family="IBM Plex Mono", size=9, color="#c9d9f0"),
                ))
            fig_cx1.add_trace(go.Scatter(
                x=[k_star], y=[y_star * 10],
                mode="markers", name=f"Solow/Sosial k* = {k_star:.3f}",
                marker=dict(color="#ffd700", size=18, symbol="star"),
            ))
            fig_cx1.add_vline(x=k_star, line_dash="dot", line_color="#ffd700", opacity=0.4,
                              annotation_text=f"k*={k_star:.2f}", annotation_font_color="#ffd700",
                              annotation_font_family="IBM Plex Mono")
            fig_cx1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Mono", color="#8b949e"),
                xaxis=dict(gridcolor="#21262d", title="Kapital İntensivliyi (İnv/İşYeri)"),
                yaxis=dict(gridcolor="#21262d", title="Ortalama ÜDM Artımı (%)"),
                title=dict(text="Regional Kapital İntensivliyi vs ÜDM (★ = k*)", font=dict(color="#58a6ff", size=12)),
                legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=9)),
                height=380, margin=dict(t=40, b=20),
            )
            st.plotly_chart(fig_cx1, use_container_width=True)

        with col2:
            # Paralel koordinatlar
            if len(reg_agg2) > 1:
                fig_par = go.Figure(go.Parcoords(
                    line=dict(color=reg_agg2["Sosial_Skoru"], colorscale="Viridis",
                              showscale=True, colorbar=dict(
                                  title=dict(text="Sosial Skor", font=dict(color="#8b949e")),
                                  tickfont=dict(color="#8b949e"), outlinewidth=0)),
                    dimensions=[
                        dict(label="İnvestisiya",   values=reg_agg2["İnvestisiya"]),
                        dict(label="İş Yerləri",    values=reg_agg2["İş_Yerləri"]),
                        dict(label="ÜDM (%)",       values=reg_agg2["ÜDM"]),
                        dict(label="Proaktiv %",    values=reg_agg2["Proaktiv"]),
                        dict(label="Məmnunluq %",   values=reg_agg2["Məmnunluq"]),
                        dict(label="K.İntens.",     values=reg_agg2["Kapital_İntensivliyi"]),
                        dict(label="Solow Norm.",   values=reg_agg2["Solow_Normlaşdırma"]),
                    ],
                ))
                fig_par.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="IBM Plex Mono", color="#c9d9f0", size=10),
                    title=dict(text="Çox Ölçülü Regional Müqayisə", font=dict(color="#58a6ff", size=12)),
                    height=380, margin=dict(t=40, b=20, l=80, r=80),
                )
                st.plotly_chart(fig_par, use_container_width=True)

        # Kross Analiz Cədvəli
        st.markdown("**Solow Normlaşdırma — Regional Uyğunluq**")
        hdr = st.columns([1.5, 1, 1, 1, 1, 1.2, 1.5])
        for col_w, h in zip(hdr, ["Region", "İnvestisiya", "İş Yerləri", "ÜDM %",
                                    "Proaktiv %", "K.İntens.", "Solow Norm."]):
            col_w.markdown(f"<div style='font-family:IBM Plex Mono;font-size:0.72rem;color:#58a6ff;font-weight:700;letter-spacing:1px;'>{h}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#21262d;margin:4px 0;'>", unsafe_allow_html=True)
        for _, row in reg_agg2.iterrows():
            nv = row["Solow_Normlaşdırma"]
            nc = "#3fb950" if nv < 1.2 else ("#ffd700" if nv < 2.0 else "#ff7b72")
            r1,r2,r3,r4,r5,r6,r7 = st.columns([1.5,1,1,1,1,1.2,1.5])
            r1.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#e6edf3;'>{row['Region']}</span>", unsafe_allow_html=True)
            r2.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#58a6ff;'>{row['İnvestisiya']:,.0f}</span>", unsafe_allow_html=True)
            r3.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#3fb950;'>{row['İş_Yerləri']:,.0f}</span>", unsafe_allow_html=True)
            r4.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#f0883e;'>{row['ÜDM']:.1f}%</span>", unsafe_allow_html=True)
            r5.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#bc8cff;'>{row['Proaktiv']:.1f}%</span>", unsafe_allow_html=True)
            r6.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#ffd700;'>{row['Kapital_İntensivliyi']:.3f}</span>", unsafe_allow_html=True)
            r7.markdown(f"<span style='font-family:IBM Plex Mono;font-size:0.82rem;color:{nc};font-weight:700;'>{nv:.2f}x {'✓' if nv<1.2 else '⚠' if nv<2.0 else '✗'}</span>", unsafe_allow_html=True)
            st.markdown("<hr style='border-color:#21262d;margin:4px 0;'>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:IBM Plex Mono;font-size:0.72rem;color:#6e7681;margin-top:8px;line-height:1.8;'>
        Solow Norm. = Kapital İntensivliyi / k* &nbsp;|&nbsp; ✓ Yaşıl &lt;1.2x (Optimal) &nbsp;|&nbsp; ⚠ Sarı 1.2–2.0x &nbsp;|&nbsp; ✗ Qırmızı &gt;2.0x (Artıq Kapital)
        </div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════╗
# ║  TAB 6 — SİVA-AI PROQNOZ MODELİ             ║
# ╚══════════════════════════════════════════════╝
with tabs[5]:
    st.markdown('<div class="sec-hdr">SİVA-AI Proqnoz Modeli — Proaktiv Xidmət Yayılma Simulyasiyası</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ibox">
    <b>SİVA-AI (Sosial İnnovasiya Vətəndaş Agentliyi — AI)</b> proaktiv xidmət yayılmasını
    <b>S-əyri (Logistik Böyümə)</b> modelinə əsasən proqnozlaşdırır. AI multiplikatoru yayılma
    sürətinə, investisiya faizi isə maksimal əhatəyə birbaşa təsir edir. Monte Carlo
    qeyri-müəyyənlik zonaları ilə birlikdə göstərilir.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Yayılma Parametrləri**")
        K_max    = st.slider("Maksimal Əhatə (% əhali)", 40, 95, 80, 5,
                             help="SİVA-AI sisteminin çata biləcəyi maksimal vətəndaş payı")
        r_speed  = st.slider("Yayılma Sürəti (r)", 0.1, 1.5, 0.5, 0.05)
        t0_inflx = st.slider("İnfleksiya İli", 2, 10, 5, 1,
                             help="S-əyrinin ən sürətli artdığı il")
        noise_level = st.slider("Qeyri-müəyyənlik Səviyyəsi (σ)", 0.5, 5.0, 2.0, 0.5)

    with col2:
        t_vals = np.linspace(0, 15, 300)
        years_ai = [2025 + t for t in t_vals]

        # AI multiplikatoru ilə gücləndirilmiş S-əyri
        ai_boost = 1 + (ai_multiplier - 1) * 0.3
        K_eff    = min(K_max * ai_boost, 97)
        sigmoid  = K_eff / (1 + np.exp(-r_speed * (t_vals - t0_inflx)))

        # Monte Carlo yayılma
        np.random.seed(int(seed_val))
        mc_sig_paths = []
        for _ in range(500):
            K_r = np.clip(np.random.normal(K_eff, K_eff * 0.05), 30, 97)
            r_r = np.clip(np.random.normal(r_speed, r_speed * 0.15), 0.05, 2.5)
            t0_r = np.clip(np.random.normal(t0_inflx, 0.8), 1, 14)
            noise = np.random.normal(0, noise_level, len(t_vals))
            path = K_r / (1 + np.exp(-r_r * (t_vals - t0_r))) + noise
            mc_sig_paths.append(np.clip(path, 0, 100))
        mc_sig_arr = np.array(mc_sig_paths)
        sig_p5  = np.percentile(mc_sig_arr, 5, axis=0)
        sig_p50 = np.percentile(mc_sig_arr, 50, axis=0)
        sig_p95 = np.percentile(mc_sig_arr, 95, axis=0)

        fig_ai = go.Figure()
        fig_ai.add_trace(go.Scatter(x=years_ai, y=sig_p95, fill=None, mode="lines",
                                    line=dict(color="rgba(88,166,255,0)"), showlegend=False))
        fig_ai.add_trace(go.Scatter(x=years_ai, y=sig_p5, fill="tonexty", mode="lines",
                                    line=dict(color="rgba(88,166,255,0)"),
                                    fillcolor="rgba(88,166,255,0.1)", name="90% Ehtimal Zonası"))
        fig_ai.add_trace(go.Scatter(x=years_ai, y=sigmoid, mode="lines", name="Deterministik S-əyri",
                                    line=dict(color="#58a6ff", width=3)))
        fig_ai.add_trace(go.Scatter(x=years_ai, y=sig_p50, mode="lines", name="MC Median",
                                    line=dict(color="#3fb950", width=1.8, dash="dot")))

        # Hədəflər
        for target_y, target_v, color in [(45, "KPI 2027: 45%", "#ffd700"),
                                           (80, "Uzunmüddətli: 80%", "#3fb950")]:
            fig_ai.add_hline(y=target_y, line_dash="dash", line_color=color, opacity=0.6,
                             annotation_text=target_v, annotation_font_color=color,
                             annotation_font_family="IBM Plex Mono", annotation_font_size=10)

        # Cari nöqtə
        fig_ai.add_trace(go.Scatter(x=[2026], y=[38.1], mode="markers",
                                    name="Faktiki 2026: 38.1%",
                                    marker=dict(color="#ffd700", size=12, symbol="diamond")))

        fig_ai.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
            font=dict(family="IBM Plex Mono", color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title="İl"),
            yaxis=dict(gridcolor="#21262d", title="Proaktiv Xidmət Əhatəsi (%)", range=[0, 100]),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d", font=dict(color="#c9d9f0", size=10)),
            title=dict(text=f"SİVA-AI Yayılma Proqnozu — Effektiv Əhatə: {K_eff:.1f}%  (AI×{ai_multiplier:.1f})",
                       font=dict(color="#58a6ff", size=13)),
            height=400, margin=dict(t=50, b=20),
        )
        st.plotly_chart(fig_ai, use_container_width=True)

    # İnfleksiya analizi
    st.markdown('<div class="sec-hdr">Sürət Analizi — Maksimal Yayılma Nöqtəsi</div>', unsafe_allow_html=True)
    inflx_rate = r_speed * K_eff / 4

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, color) in zip([c1,c2,c3,c4], [
        (f"{K_eff:.1f}%", f"AI ilə effektiv əhatə (×{ai_multiplier:.1f})", "#58a6ff"),
        (f"{inflx_rate:.2f}%/il", "İnfleksiya nöqtəsindəki maksimal sürət", "#3fb950"),
        (f"{2025 + t0_inflx}", "Ən sürətli artım ili (infleksiya)", "#f0883e"),
        (f"{sig_p50[-1]:.1f}%", f"MC Median əhatə (15-ci ildə)", "#ffd700"),
    ]):
        with col:
            st.markdown(f"""
            <div class="mcard">
              <div class="mcard-accent" style="background:{color};"></div>
              <div class="mcard-val" style="color:{color}; font-size:1.5rem;">{val}</div>
              <div class="mcard-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════
st.markdown("""
<hr style="border-color:#21262d; margin: 36px 0 10px 0;">
<p style="text-align:center; font-family:'IBM Plex Mono',monospace;
   font-size:0.72rem; color:#484f58; letter-spacing:0.5px; line-height:2;">
    VXSIA Unified Analytics Dashboard v1.0  //  Sosial İnnovasiya Modeli × Solow (1956)  //<br>
    Regional ASAN Analizi  //  Monte Carlo Simulyasiyası  //  SİVA-AI Yayılma Proqnozu  //<br>
    Vətəndaşlara Xidmət və Sosial İnnovasiyalar Agentliyi  //  Azərbaycan Respublikası  //  2026
</p>
""", unsafe_allow_html=True)