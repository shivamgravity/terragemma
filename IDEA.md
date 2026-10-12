# Hacktoberfest 2026: Week 1 "Touch Grass" — Project Concepts & Roadmap

This document outlines the core concepts conceived for the **Hacktoberfest Open-Source AI Challenge: Week 1 (Touch Grass)**. The overarching philosophy of all three concepts is to **make the screen the shortest part of the experience**, allowing users to disconnect from digital noise and connect with the natural world safely and mindfully.

---

## 🌲 Concept 1: TerraGemma (Primary Focus)
### *Offline-First Backcountry & Trail Companion Powered by Gemma 3*

### The Problem
When you venture out onto trails, mountains, or wilderness reserves, cell phone reception drops to zero. Cloud-based AI assistants (ChatGPT, Claude, Gemini API) become completely useless spinning spinners. Hikers also face real hazards: misjudging daylight, getting disoriented at trail splits, encountering sudden weather changes, or dealing with wilderness injuries (tick bites, sprains, dehydration, poisonous flora). Furthermore, trail apps frequently track and upload sensitive GPS data to remote servers.

### The Solution
**TerraGemma** is an edge-native, zero-cloud expedition assistant that runs 100% locally on your laptop or mobile device using Google's open-weight **Gemma 3** (1B / 4B). It turns your device into a reliable wilderness field station without needing a single bar of cellular signal or internet connection.

### Core Features
1. **Solar Sunset & Safe Turnaround Calculator**:
   - Calculates exact sunset times, golden hour, and dusk twilight based on trail coordinates and date.
   - Computes a strict "Turnaround Point" based on hike duration, pace, and elevation change to prevent being caught in the dark unprepared.
2. **"Eyes-Up, Screen-Down" Sensory Landmark Nav**:
   - Generates 3–4 vivid physical landmark cues (e.g., *"Look for the twin split birch at mile 1.2; listen for the creek cascade before turning right"*).
   - Designed specifically so the user reads/hears it once, puts the phone in their pocket, and looks at nature instead of staring at a glowing blue screen.
3. **Offline Audio Briefing ("Listen & Pocket Phone")**:
   - Synthesizes a natural audio briefing before you step past the trailhead, letting you start hiking immediately with your hands and eyes free.
4. **Offline Wilderness First Responder & Hazard Triage**:
   - Immediate on-device triage for trail emergencies: hypothermia, dehydration, wildlife encounters (bears, snakes, wasps), poisonous plants (poison ivy/oak, stinging nettle), and sprains.
   - Powered by Gemma 3 acting as an offline emergency advisor.
5. **Interactive OpenStreetMap Trail Visualizer**:
   - Renders interactive topographic/trail maps with custom GPX/trailhead markers using open geospatial data.
6. **Zero-Cloud & High Privacy**:
   - No GPS telemetry uploaded to third-party ad trackers. 100% private and resilient.

---

## 🌿 Concept 2: FloraCast (Modular Extension)
### *Local Gardening & Permaculture Guild Planner*

### The Problem
Beginning and intermediate gardeners spend too much time researching on screens (forums, conflicting gardening blogs) instead of being outside with their hands in the soil. Timing planting based on generic calendars often fails because local frost dates and microclimates vary drastically.

### The Solution
**FloraCast** calculates exact spring/fall frost dates and uses local Gemma to formulate immediate "Plant Today" action plans, companion planting guilds (e.g., Three Sisters: corn, beans, squash), and soil amendment tasks.

### Core Features
1. **Local Frost Date Engine**: Calculates current frost vulnerability and optimal sowing windows.
2. **Companion Planting Guild Matrix**: Generates beneficial plant pairings that naturally deter pests and enrich soil without synthetic chemicals.
3. **Step-by-Step Outdoor Soil Missions**: Generates quick, actionable 15-minute garden tasks so the gardener does the work outside and logs off.
4. **Wild Foraging & Lookalike Verifier**: Teaches safe foraging identification with strict warnings for toxic lookalikes.

---

## 🍂 Concept 3: PaceLeaf (Modular Extension)
### *Fall Foliage & Scenic Run Club Route Architect*

### The Problem
Runners and walkers often stick to monotonous paved routes or constantly check GPS watches, missing out on seasonal beauty like the vibrant autumn tree canopy and crisp outdoor air.

### The Solution
**PaceLeaf** designs scenic running and walking loops optimized for tree canopy density, elevation gains, and peak fall foliage windows.

### Core Features
1. **Canopy & Foliage Peak Estimator**: Estimates peak color dates based on latitude and seasonal temperature curves.
2. **Distraction-Free Audio Cadence Briefing**: Replaces constant turn-by-turn phone glancing with audio milestone anchors.
3. **Run Club Group Export**: Generates printable cue sheets and shareable route summaries for community outdoor groups.

---

## Technical Stack & Prize Category Alignment
- **Open-Weight AI**: Google Gemma 3 (`gemma3:1b` for lightning-fast edge response; `gemma3:4b` for deep analytical extraction) via local Ollama.
- **Frontend / UX**: Streamlit with custom outdoor-themed UI (Forest greens, earth tones, responsive cards).
- **Geospatial & Visuals**: PyDeck / Folium / OpenStreetMap open geospatial mapping.
- **Resilience / Cloud Demo**: Dual-mode engine that connects to local Ollama on-device while providing a built-in mock fallback for Streamlit Cloud demos without downtime.
- **Target Category**: **Best Use of Gemma ($200 USD)** + Hacktoberfest Overall Winner.
