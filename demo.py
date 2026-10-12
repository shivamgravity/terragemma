"""
🌲 TerraGemma — Terminal Demo & Backcountry Simulation
Run standalone without a browser: python demo.py
"""

import time
from core.solar_calculator import calculate_solar_times, calculate_turnaround_plan
from core.gemma_engine import gemma
from core.survival_triage import assess_emergency
from core.flora_fauna import FIELD_KNOWLEDGE_BASE


def run_terminal_demo():
    print("=" * 70)
    print("🌲 TERRAGEMMA • OFFLINE EDGE AI WILDERNESS FIELD STATION")
    print("   Hacktoberfest 2026: Week 1 'Touch Grass'")
    print("   Powered by Google Gemma 3 (100% On-Device / Zero Cloud)")
    print("=" * 70)
    print()

    # 1. Solar Engine & Naismith Turnaround
    print("[1/4] ⏱️ ASTRONOMICAL SOLAR & TURNAROUND ENGINE")
    print("-" * 50)
    trail_name = "Franconia Ridge Loop (White Mountains, NH)"
    lat, lon = 44.1423, -71.6811
    distance_miles = 8.9
    elevation_gain_ft = 3800
    dep_time = "08:30"

    print(f"📍 Trail: {trail_name}")
    print(f"📊 Distance: {distance_miles} mi | Elevation Gain: {elevation_gain_ft} ft")
    print(f"🚀 Planned Departure: {dep_time}")
    print()

    solar = calculate_solar_times(lat, lon)
    plan = calculate_turnaround_plan(distance_miles, elevation_gain_ft, dep_time, solar, base_pace_mph=2.5)

    print(f"   • Sunrise:              {solar['sunrise']}")
    print(f"   • Sunset:               {solar['sunset']}")
    print(f"   • Civil Dusk (Dark):    {solar['civil_dusk']}")
    print(f"   • Daylight Budget:      {solar['daylight_str']}")
    print()
    print(f"   ⭐ Hard Turnaround Time: {plan['turnaround_time']}")
    print(f"   🏁 Estimated Finish:    {plan['estimated_finish_time']}")
    print(f"   🛡️ Daylight Margin:     {plan['margin_str']}")
    print(f"   🚦 Status:              [{plan['status']}] - {plan['recommendation']}")
    print()

    # 2. Gemma 3 Edge AI Sensory Landmark Synthesis
    print("[2/4] 🎧 GEMMA 3 'EYES-UP, SCREEN-DOWN' SENSORY ANCHORS")
    print("-" * 50)
    status = gemma.check_connection()
    print(f"🤖 Active Model: {status['active_model']} ({status['mode']})")
    print("⏳ Synthesizing sensory landmarks...")
    
    t0 = time.time()
    gen = gemma.generate(
        prompt=f"Generate 3 physical sensory landmark anchors (sound, wind, visual) for {trail_name}. Turnaround time is {plan['turnaround_time']}. Keep under 150 words.",
        system_prompt="You are TerraGemma. Encourage the hiker to pocket their device and immerse in the landscape.",
        temperature=0.3
    )
    dt = round((time.time() - t0) * 1000, 1)

    print(f"⚡ Inferred via {gen['source']} in {dt} ms (Zero cloud telemetry)")
    print()
    print(gen["response"])
    print()

    # 3. Offline WFR Triage Simulation
    print("[3/4] 🚨 WILDERNESS FIRST RESPONDER (WFR) EMERGENCY TRIAGE")
    print("-" * 50)
    print("Scenario: Hiker slipped on wet granite; acute swelling at lateral ankle.")
    triage = assess_emergency(
        hazard_key="sprain_fracture",
        custom_symptoms="Severe inversion sprain on talus, unable to bear weight, no open fracture. 3 miles from trailhead.",
        trail_context=trail_name
    )
    print(f"Protocol: {triage['protocol']['title']}")
    print(f"Evacuation Urgency: {triage['protocol']['evacuation_criteria']}")
    print()

    # 4. Toxic Lookalike Protection
    print("[4/4] 🌿 TOXIC LOOKALIKE SAFETY CHECK")
    print("-" * 50)
    lookalike = FIELD_KNOWLEDGE_BASE[0] # Poison Ivy vs Virginia Creeper
    print(f"⚠️ Comparison: {lookalike['name']}")
    print(f"   • Toxic:     {lookalike['toxic_plant']}")
    print(f"   • Harmless:  {lookalike['harmless_lookalike']}")
    print(f"   • Key Rule:  {lookalike['key_differences'][0]}")
    print()

    print("=" * 70)
    print("✅ DEMO COMPLETE: Screen time minimized. Now put the laptop down and touch grass! 🌲")
    print("=" * 70)


if __name__ == "__main__":
    run_terminal_demo()
