"""
Field Flora, Fauna & Toxic Lookalike Identification
Teaches nature observation, botanical identifiers, and toxic lookalike safety offline.
"""

from typing import Dict, Any, List
from core.gemma_engine import gemma


FIELD_KNOWLEDGE_BASE = [
    {
        "name": "Poison Ivy vs. Virginia Creeper",
        "category": "Toxic Plant Lookalike",
        "danger_level": "High (Severe Contact Dermatitis)",
        "toxic_plant": "Poison Ivy (*Toxicodendron radicans*)",
        "harmless_lookalike": "Virginia Creeper (*Parthenocissus quinquefolia*)",
        "key_differences": [
            "Leaf count: Poison Ivy has clusters of THREE leaflets ('Leaves of three, let it be'). Virginia Creeper has FIVE leaflets radiating from a central stem.",
            "Middle stalk: The middle leaflet of Poison Ivy has a distinctly longer petiole (stem) than the two side leaflets.",
            "Stem/vine: Mature Poison Ivy vines have dense, hairy aerial roots clinging to tree bark ('Hairy vine, no friend of mine'). Virginia Creeper has clean tendrils with small adhesive pads.",
            "Berries: Poison Ivy produces waxy white/cream berries in autumn; Virginia Creeper produces dark blue/purple berries on red stems."
        ],
        "field_action": "If exposed to urushiol oil, wash with cold running stream water and friction immediately. Avoid hot water, which opens pores."
    },
    {
        "name": "Queen Anne's Lace vs. Deadly Poison Hemlock",
        "category": "Deadly Plant Lookalike",
        "danger_level": "Lethal Toxicity",
        "toxic_plant": "Poison Hemlock (*Conium maculatum*)",
        "harmless_lookalike": "Queen Anne's Lace / Wild Carrot (*Daucus carota*)",
        "key_differences": [
            "Stem surface: Queen Anne's Lace has hairy, green, grooved stems ('The Queen has hairy legs'). Poison Hemlock has smooth, hollow stems with characteristic purple splotches/mottling.",
            "Flower center: Queen Anne's Lace typically features a single tiny dark purple or red flower in the dead center of the umbel.",
            "Scent: Crushed Queen Anne's Lace smells pleasantly like fresh carrots. Poison Hemlock has a musty, rank, rodent-like odor.",
            "Bracts: Queen Anne's Lace has distinctive three-pronged, fern-like bracts directly beneath the flower head."
        ],
        "field_action": "POISON HEMLOCK IS FATAL IF INGESTED. Never touch or graze on wild carrot-like umbels without 100% confirmation."
    },
    {
        "name": "Blackberry vs. Baneberry",
        "category": "Berries & Foraging",
        "danger_level": "High Toxicity (Baneberry)",
        "toxic_plant": "Baneberry / Doll's Eyes (*Actaea pachypoda*)",
        "harmless_lookalike": "Wild Blackberry (*Rubus fruticosus*)",
        "key_differences": [
            "Growth habit: Wild Blackberries grow on thorny, arched canes (brambles). Baneberry grows as an herbaceous shrub with smooth stems without thorns.",
            "Berry structure: Blackberries are compound aggregate drupelets. Baneberry berries are smooth, solitary porcelain-white or red globes with a distinct dark central dot ('Doll's Eye').",
            "Leaf shape: Blackberry leaves have serrated margins with prickles underneath; Baneberry has sharply toothed, compound leaves without prickles."
        ],
        "field_action": "Never eat solitary white or glossy red berries found growing in deep woodland shade."
    },
    {
        "name": "Black Bear vs. Grizzly Bear Encounter",
        "category": "Wildlife Behavior & Safety",
        "danger_level": "Severe Hazard",
        "toxic_plant": "Grizzly / Brown Bear (*Ursus arctos*)",
        "harmless_lookalike": "American Black Bear (*Ursus americanus*)",
        "key_differences": [
            "Shoulder hump: Grizzly bears possess a pronounced, muscular hump above the shoulders for digging. Black bears have no shoulder hump; their rump is higher than their shoulders.",
            "Facial profile: Grizzlies have a concave (dished-in) facial profile. Black bears have a straight, roman nose profile from forehead to snout tip.",
            "Claws: Grizzly claws are 2-4 inches long, gently curved, and light colored. Black bear claws are short (1-2 inches), sharply curved for tree climbing.",
            "Encounter Protocol: If a Black Bear approaches, stand tall, make noise, wave arms, and fight back if attacked. If a Grizzly charges, do NOT run; use bear spray at 30 feet, or drop to stomach, interlace fingers behind neck, and play dead."
        ],
        "field_action": "Carry EPA-approved bear spray on your hip or chest harness, NEVER zipped inside a backpack."
    }
]


TOUCH_GRASS_MISSIONS = [
    {
        "title": "🌲 The Conifer Scent & Resin Quest",
        "duration": "10-15 minutes",
        "mission": "Locate three different evergreen trees along the trail. Gently press a fallen needle between your fingers and smell the crushed resin. Notice the difference between the sharp citrus scent of Douglas fir, the sweet vanilla notes of Ponderosa pine, and the damp earthiness of hemlock.",
        "screen_free_tip": "Keep your hands out of your pockets and your phone stowed away. Let your sense of smell anchor you in the forest."
    },
    {
        "title": "🍂 Autumn Canopy Pigment Hunt",
        "duration": "15 minutes",
        "mission": "Find fallen leaves representing three distinct pigments: Green (chlorophyll), Yellow/Orange (carotenoids), and Deep Crimson/Purple (anthocyanins). Hold the red leaf up against the sunlight to inspect the microscopic vascular network (veins) transferring sugars.",
        "screen_free_tip": "Do not take a photo. Take 60 seconds to simply marvel at the biological architecture before returning the leaf to the soil."
    },
    {
        "title": "🪨 Lichen Symbiosis Mapping",
        "duration": "10 minutes",
        "mission": "Examine a north-facing granite rock face. Identify the three morphological forms of lichen: Crustose (paint-like crust glued to stone), Foliose (leafy, peeling lobes), and Fruticose (shrubby, coral-like branches). Touch the dry texture and consider that each lichen is an ancient partnership between fungus and algae.",
        "screen_free_tip": "Feel the cold mineral thermal mass of the stone with your palm. Connect with geologic time."
    },
    {
        "title": "👂 The 60-Second Sound Horizon",
        "duration": "5 minutes",
        "mission": "Step 5 paces off the trail tread, find a sturdy log or boulder, sit down, close your eyes, and listen for 60 seconds. Count every non-human sound: rustling dry leaves, wind gusting through the canopy, insect chirps, distant water flow, bird calls. Open your eyes only after you have counted 4 distinct sounds.",
        "screen_free_tip": "Notice how quickly your heart rate slows when your visual field is closed and auditory awareness expands."
    }
]


def identify_field_specimen(
    description: str,
    region: str,
    specimen_type: str = "plant",
    model: str = "gemma3:1b"
) -> Dict[str, Any]:
    """
    Analyzes an observed flora/fauna specimen using Gemma 3.
    """
    prompt = f"""You are a field naturalist and botanical expert.
A hiker in {region} observed the following {specimen_type}:
"{description}"

Provide a concise field evaluation:
1. 🔍 PROBABLE SPECIES CANDIDATES: List 2 most likely candidates with scientific names.
2. ⚠️ TOXIC LOOKALIKE WARNING: Is there a dangerous or poisonous lookalike they must NOT confuse this with?
3. 🌿 OBSERVABLE BOTANICAL IDENTIFIERS: What specific physical details (leaf venation, stem texture, sap, odor) should they inspect with their naked eyes right now?
4. 💡 TOUCH GRASS NOTE: An interesting ecological fact about its role in this habitat.

Keep it concise, clear, and grounded in field safety. Emphasize never consuming unknown wild specimens."""

    system_prompt = (
        "You are an offline field botanist and wildlife educator. "
        "Promote safe outdoor observation and strict toxic lookalike vigilance."
    )

    result = gemma.generate(prompt=prompt, system_prompt=system_prompt, model=model, temperature=0.3)

    return {
        "analysis": result["response"],
        "source": result["source"],
        "latency_ms": result["latency_ms"]
    }
