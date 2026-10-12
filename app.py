"""
🌲 TerraGemma — Offline Edge AI Backcountry Companion
Powered by Google Gemma 3 running locally on-device.
Hacktoberfest 2026: Week 1 "Touch Grass" Submission
"""

import json
import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

from core.solar_calculator import calculate_solar_times, calculate_turnaround_plan
from core.gemma_engine import gemma, PRIMARY_MODEL, ANALYTICAL_MODEL
from core.trail_generator import generate_sensory_field_guide, build_trail_map
from core.survival_triage import EMERGENCY_PROTOCOLS, assess_emergency
from core.flora_fauna import FIELD_KNOWLEDGE_BASE, TOUCH_GRASS_MISSIONS, identify_field_specimen
from core.audio_briefing import render_audio_briefing_html


# ---------------- PAGE CONFIG & STYLING ----------------
st.set_page_config(
    page_title="TerraGemma • Offline Edge AI Trail Companion",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom outdoor aesthetic CSS
st.markdown("""
<style>
    /* Main container and theme accents */
    .stApp {
        background-color: #fbfbf8;
        color: #1c281f;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3a1e !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 700;
    }
    
    /* Highlight Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    
    .status-badge-safe {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    
    .status-badge-caution {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    
    .status-badge-hazard {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    
    .screen-free-banner {
        background: linear-gradient(90deg, #1e3a1e 0%, #2d5a27 100%);
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- DATA INITIALIZATION ----------------
@st.cache_data
def load_sample_trails():
    data_path = os.path.join(os.path.dirname(__file__), "data", "sample_trails.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

trails = load_sample_trails()


# ---------------- SIDEBAR: GEMMA & PRIVACY TELEMETRY ----------------
with st.sidebar:
    st.markdown("## 🌲 TerraGemma")
    st.caption("Offline Edge AI Wilderness Field Guide")
    st.markdown("---")
    
    # Check Ollama Status
    status = gemma.check_connection()
    if status["online"]:
        st.success(f"🟢 **Edge Model Active:** `{status['active_model']}`")
    else:
        st.warning(f"🟡 **Offline Resilient Mode:** `{status['active_model']}`")
        
    st.markdown("### ⚙️ Edge AI Configuration")
    selected_model = st.selectbox(
        "Gemma 3 Architecture:",
        options=[PRIMARY_MODEL, ANALYTICAL_MODEL],
        index=0,
        help="Gemma 3 (1B) is optimized for ultra-fast low-power edge devices. Gemma 3 (4B) provides deeper reasoning."
    )
    gemma.preferred_model = selected_model

    st.markdown("---")
    st.markdown("### 🔒 Zero-Cloud Guarantee")
    st.info(
        "**100% Private & Signal-Free**\n\n"
        "• Zero cloud API calls\n"
        "• GPS coordinates stay on device\n"
        "• Works in airplane mode / deep backcountry"
    )
    
    if gemma.last_latency_ms is not None:
        st.metric(
            label="Last Edge Inference Latency",
            value=f"{gemma.last_latency_ms} ms",
            delta=gemma.last_source
        )

    st.markdown("---")
    st.caption("Built for Hacktoberfest 2026: Week 1 'Touch Grass'")


# ---------------- MAIN APP HEADER ----------------
st.title("🌲 TerraGemma • Backcountry Expedition Assistant")
st.markdown(
    "**The screen should be the shortest part of your outdoor experience.** "
    "TerraGemma combines **astronomical solar math**, **Naismith's turnaround rules**, "
    "and **Google Gemma 3 running locally** to give you sensory navigation cues and emergency triage—so you can put your phone in your pocket and touch grass."
)

st.markdown("""
<div class="screen-free-banner">
    <div>
        <b>🌿 Philosophy: Eyes Up, Screen Down.</b>
        <span style="opacity: 0.9; margin-left: 8px;">Check your turnaround time, listen to your audio briefing, and stow your phone.</span>
    </div>
    <div style="font-size: 20px;">📵 ➜ 🌲</div>
</div>
""", unsafe_allow_html=True)


# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 Expedition Planner & Turnaround",
    "🚨 Wilderness First Responder (Triage)",
    "🌿 Field Flora, Fauna & Missions",
    "📊 Open AI Architecture & Telemetry"
])


# ========================================================
# TAB 1: EXPEDITION PLANNER & SAFE TURNAROUND
# ========================================================
with tab1:
    col_input, col_map = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("1. Select or Configure Trail")
        trail_options = [t["name"] for t in trails] + ["Custom Coordinates"]
        chosen_trail_name = st.selectbox("Choose Trail:", trail_options, index=0)

        if chosen_trail_name != "Custom Coordinates":
            trail_data = next(t for t in trails if t["name"] == chosen_trail_name)
            lat = trail_data["lat"]
            lon = trail_data["lon"]
            distance_miles = float(trail_data["distance_miles"])
            elevation_gain_ft = float(trail_data["elevation_gain_ft"])
            terrain = trail_data["terrain"]
            region = trail_data["region"]
            st.caption(f"📍 **{region}** • {trail_data['highlights']}")
        else:
            trail_data = {
                "name": "Custom Trail Exploration",
                "region": "Local Wilderness",
                "lat": 37.7749,
                "lon": -122.4194,
                "distance_miles": 6.0,
                "elevation_gain_ft": 1500,
                "terrain": "Mixed Forest & Dirt Path",
                "waypoints": [{"name": "Trailhead Start", "lat": 37.7749, "lon": -122.4194, "type": "trailhead", "desc": "Departure point"}]
            }
            c_lat, c_lon = st.columns(2)
            lat = c_lat.number_input("Latitude", value=37.7749, format="%.4f")
            lon = c_lon.number_input("Longitude", value=-122.4194, format="%.4f")
            trail_data["lat"] = lat
            trail_data["lon"] = lon
            
            c_dist, c_elev = st.columns(2)
            distance_miles = c_dist.number_input("Roundtrip Distance (miles)", value=6.0, step=0.5)
            elevation_gain_ft = c_elev.number_input("Elevation Gain (feet)", value=1500, step=100)
            terrain = st.text_input("Terrain Type", value="Mixed Woodland & Creek Basin")
            region = "Custom Regional Wilderness"

        st.markdown("---")
        st.subheader("2. Hike Timing & Naismith's Rule")
        
        c_dep, c_pace = st.columns(2)
        departure_time = c_dep.time_input("Planned Departure Time", value=None)
        dep_str = departure_time.strftime("%H:%M") if departure_time else "09:00"
        
        base_pace = c_pace.slider("Base Pace (mph)", min_value=1.5, max_value=4.0, value=2.5, step=0.25,
                                  help="Average hiking speed on flat ground. Naismith's Rule automatically adds time for elevation.")

        # Compute Astronomical Solar & Turnaround
        solar = calculate_solar_times(lat, lon)
        plan = calculate_turnaround_plan(
            distance_miles=distance_miles,
            elevation_gain_ft=elevation_gain_ft,
            departure_time_str=dep_str,
            solar_info=solar,
            base_pace_mph=base_pace
        )

        # Metrics display
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Sunrise", solar["sunrise"])
        m2.metric("Sunset", solar["sunset"])
        m3.metric("Civil Dusk", solar["civil_dusk"])
        m4.metric("Daylight Total", solar["daylight_str"])

        st.markdown("---")
        st.markdown("### ⏱️ Safe Turnaround & Sunset Buffer")
        
        status_class = f"status-badge-{plan['status'].lower()}"
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span class="{status_class}">STATUS: {plan['status']}</span>
                <span style="font-size: 13px; color: #64748b;">Naismith Estimated Duration: <b>{plan['estimated_duration_str']}</b></span>
            </div>
            <div style="display: flex; gap: 20px; align-items: baseline;">
                <div>
                    <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Hard Turnaround Time</div>
                    <div style="font-size: 28px; font-weight: 800; color: #1e3a1e;">{plan['turnaround_time']}</div>
                </div>
                <div style="border-left: 1px solid #e2e8f0; padding-left: 20px;">
                    <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Estimated Finish</div>
                    <div style="font-size: 22px; font-weight: 700; color: #334155;">{plan['estimated_finish_time']}</div>
                </div>
                <div style="border-left: 1px solid #e2e8f0; padding-left: 20px;">
                    <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Daylight Margin</div>
                    <div style="font-size: 22px; font-weight: 700; color: {'#166534' if plan['daylight_margin_minutes'] >= 60 else '#991b1b'};">{plan['margin_str']}</div>
                </div>
            </div>
            <p style="margin: 12px 0 0 0; font-size: 13px; color: #475569;"><b>Recommendation:</b> {plan['recommendation']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_map:
        st.subheader("🗺️ Trail Map & Waypoints (OpenStreetMap)")
        m = build_trail_map(trail_data, turnaround_time=plan["turnaround_time"])
        st_folium(m, width="100%", height=420)
        
        st.caption("Map rendered with OpenStreetMap geospatial data. Green = Trailhead, Red/Blue = High Waypoint / Checkpoints.")

    # SECTION: AI SENSORY GUIDE GENERATOR
    st.markdown("---")
    st.subheader("🎧 'Eyes-Up, Screen-Down' Field Briefing & Audio Mode")
    st.markdown(
        "Instead of glancing at a blue screen every 30 seconds, Gemma synthesizes **physical sensory cues** "
        "(stream sounds, ridge winds, rock landmarks). Generate your briefing, hit play, and put your device away."
    )

    if st.button("🌲 Synthesize Sensory Field Briefing with Gemma 3", type="primary"):
        with st.spinner(f"Gemma 3 ({selected_model}) generating sensory anchors locally..."):
            guide = generate_sensory_field_guide(
                trail_name=trail_data["name"],
                region=region,
                distance_miles=distance_miles,
                elevation_gain_ft=elevation_gain_ft,
                terrain=terrain,
                turnaround_time=plan["turnaround_time"],
                sunset_time=solar["sunset"],
                model=selected_model
            )
            st.session_state["last_guide"] = guide

    if "last_guide" in st.session_state:
        g = st.session_state["last_guide"]
        
        # Audio Player Component (Web Speech API)
        audio_html = render_audio_briefing_html(
            text_to_speak=g["audio_script"],
            title=f"{trail_data['name']} Audio Briefing",
            turnaround_time=g["turnaround_time"]
        )
        components.html(audio_html, height=215, scrolling=False)

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Written Field Briefing & Landmark Anchors")
        st.markdown(g["guide_markdown"])
        st.caption(f"⚡ Inferred via {g['source']} in {g['latency_ms']} ms • Zero telemetry transmitted.")


# ========================================================
# TAB 2: WILDERNESS FIRST RESPONDER TRIAGE
# ========================================================
with tab2:
    st.subheader("🚨 Offline Wilderness First Responder (WFR) Hazard Triage")
    st.markdown(
        "In deep backcountry with zero cellular signal, emergency medical decisions cannot wait. "
        "Select a hazard or describe symptoms below for instant, offline triage guidance powered by Gemma 3."
    )

    col_triage_sel, col_triage_act = st.columns([1, 1], gap="large")

    with col_triage_sel:
        hazard_keys = list(EMERGENCY_PROTOCOLS.keys())
        hazard_titles = [EMERGENCY_PROTOCOLS[k]["title"] for k in hazard_keys]
        selected_title = st.selectbox("Select Emergency Hazard:", hazard_titles, index=0)
        selected_key = hazard_keys[hazard_titles.index(selected_title)]
        proto = EMERGENCY_PROTOCOLS[selected_key]

        st.markdown(f"### {proto['title']}")
        st.markdown(f"**Primary Indicators:** {proto['primary_symptoms']}")

        st.markdown("#### ✅ Immediate Field Protocol:")
        for action in proto["immediate_actions"]:
            st.markdown(f"- {action}")

        st.markdown("#### 🚫 Critical Contraindications (What NOT To Do):")
        for contra in proto["contraindications"]:
            st.markdown(f"- {contra}")

        st.warning(f"**Evacuation Urgency:** {proto['evacuation_criteria']}")

    with col_triage_act:
        st.markdown("### 🔍 Live Symptom Evaluation (Gemma 3)")
        custom_symptoms = st.text_area(
            "Describe the hiker's specific observed symptoms or dilemma:",
            value="Hiker stumbled on a loose talus slope. Left ankle is swelling rapidly, cannot bear weight on heel, but toes have normal sensation. We are 3.5 miles from the trailhead with 2 hours of daylight left.",
            height=120
        )
        trail_env = st.text_input("Current Trail & Weather Context:", value=f"{trail_data['name']} • High elevation alpine ridge")

        if st.button("Evaluate Medical Triage Offline", type="primary"):
            with st.spinner("Gemma 3 performing offline wilderness triage assessment..."):
                triage_res = assess_emergency(
                    hazard_key=selected_key,
                    custom_symptoms=custom_symptoms,
                    trail_context=trail_env,
                    model=selected_model
                )
                st.session_state["last_triage"] = triage_res

        if "last_triage" in st.session_state:
            t = st.session_state["last_triage"]
            st.markdown("---")
            st.markdown(t["ai_assessment"])
            st.caption(f"⚡ Evaluated offline via {t['source']} in {t['latency_ms']} ms.")


# ========================================================
# TAB 3: FIELD FLORA, FAUNA & TOUCH GRASS MISSIONS
# ========================================================
with tab3:
    st.subheader("🌿 Field Flora, Fauna & Toxic Lookalike Safety")
    st.markdown(
        "Observe the wild world with clarity and safety. Review critical toxic lookalikes before foraging or touching wild species."
    )

    t_sub1, t_sub2, t_sub3 = st.tabs([
        "⚠️ Toxic Lookalike Comparisons",
        "🎯 Mindful 'Touch Grass' Missions",
        "🔍 Specimen Identifier Assistant"
    ])

    with t_sub1:
        for item in FIELD_KNOWLEDGE_BASE:
            with st.expander(f"**{item['name']}** — {item['category']} ({item['danger_level']})", expanded=False):
                c_tox, c_safe = st.columns(2)
                c_tox.error(f"**Toxic / Dangerous:** {item['toxic_plant']}")
                c_safe.success(f"**Lookalike / Benign:** {item['harmless_lookalike']}")
                
                st.markdown("#### Key Botanical / Morphological Differences:")
                for diff in item["key_differences"]:
                    st.markdown(f"- {diff}")
                    
                st.info(f"**Field Action:** {item['field_action']}")

    with t_sub2:
        st.markdown("### 🎒 Screen-Free Observational Missions")
        st.markdown("Try one of these four mindful nature missions to deepen your outdoor experience:")
        
        m_cols = st.columns(2)
        for i, mission in enumerate(TOUCH_GRASS_MISSIONS):
            with m_cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0 0 6px 0; color: #1e3a1e;">{mission['title']}</h4>
                    <span style="font-size: 12px; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{mission['duration']}</span>
                    <p style="margin: 10px 0; font-size: 13px; line-height: 1.5; color: #334155;">{mission['mission']}</p>
                    <div style="font-size: 12px; color: #15803d; font-weight: 500;">🌿 <b>Screen-Free Tip:</b> {mission['screen_free_tip']}</div>
                </div>
                """, unsafe_allow_html=True)

    with t_sub3:
        st.markdown("### 🔍 Query Specimen Identification")
        st.caption("Describe physical features (bark texture, leaf venation, spore structures, bird vocalization) for offline analysis.")
        
        spec_desc = st.text_area(
            "Describe the sighting:",
            value="Tall biennial plant with umbrella-shaped clusters of tiny white flowers. Stem is smooth with noticeable purple blotches and smells unpleasant when bruised.",
            height=100
        )
        spec_region = st.text_input("Region / Habitat:", value="Damp woodland ditch, Pacific Northwest")

        if st.button("Identify Specimen Offline", type="secondary"):
            with st.spinner("Gemma 3 analyzing botanical identifiers..."):
                spec_res = identify_field_specimen(
                    description=spec_desc,
                    region=spec_region,
                    model=selected_model
                )
                st.session_state["last_spec"] = spec_res

        if "last_spec" in st.session_state:
            sp = st.session_state["last_spec"]
            st.markdown("---")
            st.markdown(sp["analysis"])
            st.caption(f"⚡ Inferred via {sp['source']} in {sp['latency_ms']} ms.")


# ========================================================
# TAB 4: WHY OPEN INNOVATION MATTERS
# ========================================================
with tab4:
    st.subheader("📊 Why Open Innovation Matters for Backcountry Wilderness")
    st.markdown(
        "Open-weight models are not just a nice-to-have for outdoor explorers—**they are the only architecture that genuinely works** when you step off the grid."
    )

    c_why1, c_why2 = st.columns(2)

    with c_why1:
        st.markdown("""
        ### 1. 📶 Zero-Connectivity Resilience
        Cloud APIs (OpenAI, Anthropic, Gemini Cloud API) require persistent internet connections. 
        In national parks, alpine passes, and wilderness valleys, cell signal drops to 0 bars. 
        **Closed APIs fail completely.** Open-weight models like **Gemma 3 (1B / 4B)** run natively on consumer silicon, turning a laptop, tablet, or edge hardware into an autonomous wilderness field station with no towers required.
        
        ### 2. 🛡️ Absolute Location & Medical Privacy
        Outdoor trail apps frequently package high-precision GPS tracks, departure times, and personal health data and sell them to ad brokers or telemetry vendors. 
        TerraGemma executes 100% locally: your coordinates, medical triage notes, and trail logs **never leave your device**.
        """)

    with c_why2:
        st.markdown("""
        ### 3. 💸 Zero API Bills & Unlimited Offline Utility
        Closed APIs charge per thousand tokens and enforce aggressive rate limits. 
        If you are on a 5-day backcountry trip, an open-weight model costs **$0.00** in API fees, never hits usage limits, and consumes minimal power.
        
        ### 4. ⚡ Quantized Lightweight Edge Efficiency
        Google's **Gemma 3 (1B)** model requires under 1 GB of memory, enabling real-time generation in hundreds of milliseconds directly on CPU or edge hardware—leaving your device battery intact for navigation and safety.
        """)

    st.markdown("---")
    st.subheader("🛠️ Architecture & System Topology")
    
    st.markdown("""
    ```mermaid
    flowchart TD
        A["Hiker at Trailhead (Zero Cell Reception)"] --> B["TerraGemma App (Local Streamlit)"]
        B --> C["NOAA Solar Engine (Sunset & Turnaround Math)"]
        B --> D["OpenStreetMap Engine (Topographic Layers & Waypoints)"]
        B --> E["Gemma 3 Edge Engine (Ollama / Local Weights)"]
        E --> F["Sensory Landmark Synthesis ('Eyes-Up Guide')"]
        E --> G["Wilderness First Responder (Triage Matrix)"]
        E --> H["Field Flora & Toxic Lookalike Identification"]
        F --> I["Web Speech API Audio Synthesizer"]
        I --> J["Hiker Listens, Pockets Phone & Touches Grass 🌲"]
    ```
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🏆 Hacktoberfest 2026 Partner Category Alignment")
    st.markdown("""
    - **Featured Category: Best Use of Gemma ($200 USD)**:
      TerraGemma is built entirely around Google's open-weight **Gemma 3 (1B and 4B)** served locally through Ollama. Gemma powers dynamic sensory landmark generation, structured WFR triage evaluation, and offline botanical identification without any proprietary cloud dependencies.
    """)
