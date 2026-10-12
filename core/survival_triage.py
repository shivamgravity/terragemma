"""
Wilderness First Responder (WFR) & Hazard Triage System
100% offline edge medical & survival assessment powered by Gemma 3.
"""

from typing import Dict, Any, List
from core.gemma_engine import gemma


EMERGENCY_PROTOCOLS = {
    "hypothermia": {
        "title": "🥶 Hypothermia & Cold Weather Exposure",
        "primary_symptoms": "Shivering, stumbling, mumbles, slurred speech, apathy ('The Umbles').",
        "immediate_actions": [
            "Stop hiking immediately. Insulate patient from cold ground using backpack, foam pad, or dry pine needles.",
            "Remove all wet layers and replace with dry synthetic or wool clothing.",
            "Apply the 'Hypo-Wrap': place patient in sleeping bag, sandwich warm water bottles wrapped in cloth at torso/armpits.",
            "If alert, give warm high-sugar liquids (honey water, warm tea). NEVER give alcohol or caffeine."
        ],
        "contraindications": [
            "DO NOT vigorously rub cold limbs or frostbite (causes tissue necrosis).",
            "DO NOT place warm objects directly against bare skin (causes burns).",
            "DO NOT give liquids if patient is drowsy or unable to swallow safely."
        ],
        "evacuation_criteria": "URGENT if shivering ceases while patient is still cold, mental confusion appears, or core temp fails to rebound."
    },
    "heat_illness": {
        "title": "☀️ Heat Exhaustion vs. Life-Threatening Heat Stroke",
        "primary_symptoms": "Heavy sweating, nausea, dizziness, rapid pulse (Exhaustion) VS. Confusion, collapse, seizures, hot red skin (Stroke).",
        "immediate_actions": [
            "Move patient to deep shade immediately and loosen tight clothing.",
            "Active evaporative cooling: soak shirt/bandana in stream water and fan vigorously.",
            "Elevate feet 8-12 inches to restore blood flow to core organs.",
            "Small sips of electrolyte water every 10 minutes if alert."
        ],
        "contraindications": [
            "DO NOT administer salt tablets directly (worsens stomach cramps and dehydration).",
            "DO NOT allow patient to resume hiking today even if feeling somewhat recovered."
        ],
        "evacuation_criteria": "CRITICAL EMERGENCY if altered mental status, delirium, or loss of consciousness occurs. Evacuate immediately."
    },
    "snakebite": {
        "title": "🐍 Venomous Snakebite (Pit Vipers / Rattlesnakes / Adders)",
        "primary_symptoms": "Puncture marks, rapid burning pain, progressive swelling, metallic taste, nausea.",
        "immediate_actions": [
            "Keep patient completely calm and still. Movement accelerates lymphatic venom circulation.",
            "Remove rings, watches, boots, and tight clothing before swelling sets in.",
            "Immobilize the bitten limb with a loose splint and position at neutral heart level.",
            "Mark the leading edge of swelling with a pen/charcoal every 15 minutes with timestamps.",
            "Plan a non-strenuous carry-out evacuation or trigger emergency SOS signal."
        ],
        "contraindications": [
            "DO NOT cut the wound or try to suck venom out (movies are wrong; this damages tissue).",
            "DO NOT apply a tourniquet or arterial constricting band.",
            "DO NOT apply ice or electric shock."
        ],
        "evacuation_criteria": "EMERGENCY: All venomous snakebites require professional antivenom therapy at an acute medical facility."
    },
    "stings_allergies": {
        "title": "🐝 Insect Stings & Anaphylaxis",
        "primary_symptoms": "Localized pain/redness VS. Hives, lip/throat swelling, wheezing, dizziness (Systemic Anaphylaxis).",
        "immediate_actions": [
            "Scrape stinger away sideways with a credit card edge or dull knife. Avoid pinching venom sac.",
            "If signs of anaphylaxis appear (difficulty breathing, throat tightness), administer patient's EpiPen (epinephrine auto-injector) into outer thigh immediately.",
            "Hold auto-injector in place for 3 full seconds, massage injection site for 10 seconds.",
            "Position patient sitting upright if breathing difficulty, or lying down with elevated feet if dizzy."
        ],
        "contraindications": [
            "DO NOT hesitate to use epinephrine. Waiting is the leading cause of fatal outdoor anaphylaxis.",
            "DO NOT squeeze the stinger with tweezers (injects remaining venom)."
        ],
        "evacuation_criteria": "URGENT: Any anaphylactic reaction requires immediate evacuation even if epinephrine temporarily resolves symptoms."
    },
    "sprain_fracture": {
        "title": "🦶 Ankle Sprains, Fractures & Musculoskeletal Trauma",
        "primary_symptoms": "Inability to bear weight, severe pain on palpation, rapid swelling, deformity.",
        "immediate_actions": [
            "Perform 'Ottawa Ankle Rules' check: Can patient bear weight for 4 steps? Palpate posterior 6cm of malleoli.",
            "If severe sprain/fracture suspected, immobilize using improvised sam-splint or sturdy sticks padded with clothing.",
            "Secure splint with bandanas, webbing, or duct tape above and below injury.",
            "Elevate limb on pack during rest breaks; apply cold stream water compresses (15 min on, 15 min off)."
        ],
        "contraindications": [
            "DO NOT remove boot on the trail if patient must walk out under their own power (the boot acts as a natural splint).",
            "DO NOT attempt to reduce/straighten compound (bone protruding) fractures in the field."
        ],
        "evacuation_criteria": "MODERATE to URGENT: If deformity present, numbness/cold toes (loss of pulse), or completely non-ambulatory."
    },
    "lost_navigation": {
        "title": "🧭 Disorientation / Lost on the Trail (S.T.O.P. Protocol)",
        "primary_symptoms": "Uncertainty of trail markers, missing landmarks, dusk approaching, anxiety.",
        "immediate_actions": [
            "**S - STOP:** Sit down immediately. Panic causes rash decisions, energy depletion, and trail departure.",
            "**T - THINK:** When was your last confirmed landmark? How much daylight remains? Check your turnaround deadline.",
            "**O - OBSERVE:** Look for prominent terrain features, wind direction, water drainages, footprints, sun position.",
            "**P - PLAN:** If trail is nearby and daylight allows, backtrack carefully. If daylight is fading, prepare a bivouac shelter before dark.",
            "**Signal:** 3 distinct whistle blasts or 3 mirror flashes spaced evenly (international distress signal). Repeat every 5 minutes."
        ],
        "contraindications": [
            "DO NOT wander aimlessly or bushwhack in panic, especially downhill into dense brush.",
            "DO NOT separate hiking partners."
        ],
        "evacuation_criteria": "Stay in place. Search & Rescue teams find stationary lost hikers 4x faster than moving hikers."
    }
}


def assess_emergency(
    hazard_key: str,
    custom_symptoms: str,
    trail_context: str,
    model: str = "gemma3:1b"
) -> Dict[str, Any]:
    """
    Evaluates emergency situation with Gemma 3, combining formal WFR protocol with dynamic symptoms.
    """
    protocol = EMERGENCY_PROTOCOLS.get(hazard_key, EMERGENCY_PROTOCOLS["lost_navigation"])
    
    prompt = f"""You are a certified Wilderness Emergency First Responder (WFR).
A hiker in the backcountry with NO CELL SERVICE is reporting a medical/survival emergency.

Standard Protocol Baseline for {protocol['title']}:
Primary Symptoms: {protocol['primary_symptoms']}
Key Actions: {', '.join(protocol['immediate_actions'][:2])}
Contraindications: {', '.join(protocol['contraindications'][:2])}

Current Hiker Report:
- Context/Trail: {trail_context}
- Specific Observed Symptoms/Situation: {custom_symptoms}

Provide a structured, authoritative emergency response:
1. 🚨 IMMEDIATE 3-STEP TRIAGE ACTION (What to do in the first 5 minutes)
2. ⚠️ CRITICAL CONTRAINDICATIONS (Things that will make this worse)
3. ⏱️ EVACUATION DECISION (Can they hike out, assisted carry, or stay put and signal SOS?)
4. 📢 RESCUE SIGNALING GUIDANCE (Whistle/mirror/ground marker steps)

Keep advice clear, numbered, and calm. Do not use generic filler words."""

    system_prompt = (
        "You are an offline wilderness emergency triage agent. "
        "Prioritize life safety, hypothermia prevention, and sound backcountry medical judgment. "
        "Be concise, direct, and actionable."
    )

    result = gemma.generate(prompt=prompt, system_prompt=system_prompt, model=model, temperature=0.2)

    return {
        "protocol": protocol,
        "ai_assessment": result["response"],
        "source": result["source"],
        "latency_ms": result["latency_ms"]
    }
