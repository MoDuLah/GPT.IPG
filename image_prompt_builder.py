from __future__ import annotations

import json
import random
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "Image Prompt Builder"
ORG_NAME = "MoDuL"
PRESET_VERSION = 1

NS = "Not specified"

IMAGE_TYPES = [
    NS,
    "Illustration",
    "Concept art",
    "Graphic novel artwork",
    "Comic panel",
    "Comic page",
    "Poster",
    "Book cover",
    "Logo",
    "UI element",
    "Icon",
    "Character portrait",
    "Character sheet",
    "Environment art",
    "Product image",
]
ASPECTS = [
    NS,
    "1:1 square",
    "16:9 widescreen",
    "9:16 vertical",
    "4:5 portrait",
    "3:2 landscape",
    "2:3 portrait",
    "A4 portrait",
    "A4 landscape",
    "Comic page portrait",
    "Ultra-wide banner",
]
BACKGROUND_TYPES = [
    NS,
    "Fully illustrated background",
    "Transparent background",
    "Plain solid background",
    "Green chroma-key background",
    "White studio background",
    "Black studio background",
    "Soft gradient background",
]
SUBJECT_TYPES = [
    NS,
    "Single person",
    "Two people",
    "Group of people",
    "Creature",
    "Animal",
    "Vehicle",
    "Object",
    "Building",
    "Landscape",
    "Abstract concept",
]
AGES = [NS, "Child", "Teenager", "Young adult", "Adult", "Middle-aged", "Older adult"]
POSES = [
    NS,
    "Neutral standing pose",
    "Confident standing pose",
    "Walking",
    "Running",
    "Sitting",
    "Crouching",
    "Fighting stance",
    "Dynamic action pose",
    "Looking over shoulder",
    "Leaning against an object",
]
EXPRESSIONS = [
    NS,
    "Neutral",
    "Calm",
    "Confident",
    "Determined",
    "Angry",
    "Fearful",
    "Sad",
    "Happy",
    "Suspicious",
    "Surprised",
    "Exhausted",
]
GAZES = [
    NS,
    "Facing camera",
    "Looking left",
    "Looking right",
    "Looking upward",
    "Looking downward",
    "Looking away from camera",
    "Back to camera",
    "Three-quarter view",
    "Profile view",
]
SHOTS = [
    NS,
    "Extreme close-up",
    "Close-up",
    "Head-and-shoulders portrait",
    "Bust shot",
    "Half-body shot",
    "Three-quarter body shot",
    "Full-body shot",
    "Wide shot",
    "Extreme wide establishing shot",
    "Over-the-shoulder shot",
    "Two-shot",
]
ANGLES = [
    NS,
    "Eye level",
    "Low angle",
    "High angle",
    "Overhead",
    "Bird's-eye view",
    "Worm's-eye view",
    "Dutch angle",
    "Ground-level angle",
]
PERSPECTIVES = [
    NS,
    "Natural perspective",
    "Wide-angle perspective",
    "Telephoto compression",
    "Macro perspective",
    "Isometric",
    "Orthographic",
    "One-point perspective",
    "Two-point perspective",
    "Three-point perspective",
    "Fisheye lens",
]
PLACEMENTS = [
    NS,
    "Centred",
    "Left third",
    "Right third",
    "Lower third",
    "Upper third",
    "Foreground",
    "Midground",
    "Background",
    "Symmetrical composition",
    "Asymmetrical composition",
]
DOF = [
    NS,
    "Shallow depth of field",
    "Moderate depth of field",
    "Deep focus",
    "Everything sharply focused",
    "Soft blurred background",
]
SETTING_TYPES = [
    NS,
    "Interior",
    "Exterior",
    "Urban",
    "Rural",
    "Industrial",
    "Natural landscape",
    "Underground",
    "Space",
    "Underwater",
    "Surreal environment",
]
PERIODS = [
    NS,
    "Ancient",
    "Medieval",
    "Victorian",
    "1920s",
    "1950s",
    "1980s",
    "1990s",
    "Contemporary",
    "Near future",
    "Distant future",
    "Post-apocalyptic",
]
TIMES = [
    NS,
    "Dawn",
    "Morning",
    "Midday",
    "Afternoon",
    "Golden hour",
    "Sunset",
    "Blue hour",
    "Night",
    "Midnight",
]
WEATHER = [
    NS,
    "Clear",
    "Cloudy",
    "Overcast",
    "Light rain",
    "Heavy rain",
    "Thunderstorm",
    "Snow",
    "Fog",
    "Windy",
    "Dust storm",
]
LIGHTING = [
    NS,
    "Natural daylight",
    "Soft cinematic lighting",
    "Hard cinematic lighting",
    "Studio lighting",
    "Neon lighting",
    "Moonlight",
    "Candlelight",
    "Firelight",
    "Fluorescent lighting",
    "Volumetric lighting",
    "Silhouette lighting",
]
LIGHT_DIRECTIONS = [
    NS,
    "Front-lit",
    "Backlit",
    "Side-lit from left",
    "Side-lit from right",
    "Top-lit",
    "Under-lit",
    "Rim lighting",
    "Three-point lighting",
]
TEMPERATURES = [
    NS,
    "Warm",
    "Cool",
    "Neutral",
    "Mixed warm and cool",
    "Cold blue",
    "Golden amber",
    "Green fluorescent cast",
    "Magenta and cyan neon",
]
CONTRASTS = [
    NS,
    "Low contrast",
    "Medium contrast",
    "High contrast",
    "Deep dramatic shadows",
    "Soft shadows",
    "Hard-edged shadows",
]
ATMOSPHERES = [
    NS,
    "None",
    "Light fog",
    "Dense fog",
    "Smoke",
    "Dust particles",
    "Rain streaks",
    "Snow particles",
    "Volumetric light rays",
    "Lens flare",
    "Heat haze",
]
ART_STYLES = [
    NS,
    "Photorealistic",
    "Cinematic realism",
    "Graphic novel",
    "Western comic-book art",
    "Heavy black-ink comic art",
    "Anime",
    "Manga",
    "Cel-shaded illustration",
    "3D render",
    "Painterly digital art",
    "Oil painting",
    "Watercolour",
    "Pixel art",
    "Flat vector art",
    "Retro poster art",
    "Concept sketch",
]
LINEWORK = [
    NS,
    "No visible linework",
    "Clean thin lines",
    "Bold clean outlines",
    "Heavy black inks",
    "Loose sketch lines",
    "Angular linework",
    "Cross-hatched inks",
    "Brush-pen linework",
]
SHADING = [
    NS,
    "Flat colours",
    "Cel shading",
    "Soft gradient shading",
    "Painterly shading",
    "Cross-hatching",
    "Halftone shading",
    "Chiaroscuro",
    "Minimal shading",
]
DETAIL = [
    NS,
    "Minimal",
    "Clean and simple",
    "Moderately detailed",
    "Highly detailed",
    "Extremely intricate",
    "Detailed subject, simplified background",
]
MOODS = [
    NS,
    "Mysterious",
    "Dark and bleak",
    "Tense",
    "Heroic",
    "Epic",
    "Hopeful",
    "Peaceful",
    "Romantic",
    "Threatening",
    "Melancholic",
    "Playful",
    "Surreal",
]
PALETTES = [
    NS,
    "Full colour",
    "Monochrome",
    "Black and white",
    "Duotone",
    "Muted palette",
    "Vibrant palette",
    "Pastel palette",
    "Neon palette",
    "Earth tones",
    "Cold palette",
    "Warm palette",
    "Limited comic palette",
]
SATURATION = [
    NS,
    "Desaturated",
    "Slightly muted",
    "Natural saturation",
    "Rich saturation",
    "Highly saturated",
]
FONTS = [
    NS,
    "Modern sans-serif",
    "Bold condensed sans-serif",
    "Classic serif",
    "Elegant serif",
    "Handwritten",
    "Comic lettering",
    "Futuristic",
    "Distressed",
    "Stencil",
    "Monospaced terminal",
    "No text",
]
TEXT_PLACEMENT = [
    NS,
    "Top centre",
    "Top left",
    "Top right",
    "Centre",
    "Bottom centre",
    "Bottom left",
    "Bottom right",
    "Inside speech bubble",
    "Inside caption box",
    "Integrated into environment",
]

MONITOR_POSITIONS = [
    ("Top left", "top-left position on the monitor"),
    ("Top centre", "top-centre position on the monitor"),
    ("Top right", "top-right position on the monitor"),
    ("Middle left", "middle-left position on the monitor"),
    ("Centre", "centre position on the monitor"),
    ("Middle right", "middle-right position on the monitor"),
    ("Bottom left", "bottom-left position on the monitor"),
    ("Bottom centre", "bottom-centre position on the monitor"),
    ("Bottom right", "bottom-right position on the monitor"),
]

APPEARANCE_OPTIONS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Build and Body": [
            "slim build",
            "lean build",
            "athletic build",
            "muscular build",
            "stocky build",
            "broad-shouldered build",
            "narrow-shouldered build",
            "curvy build",
            "plus-size build",
            "delicate frame",
            "powerful frame",
            "tall stature",
            "short stature",
            "average height",
            "long limbs",
            "compact proportions",
        ],
        "Face Shape": [
            "oval face",
            "round face",
            "square jaw",
            "heart-shaped face",
            "long face",
            "angular face",
            "soft facial structure",
            "sharp facial structure",
            "prominent cheekbones",
            "soft cheeks",
            "strong chin",
            "narrow chin",
        ],
        "Complexion and Skin": [
            "fair skin",
            "light skin",
            "olive skin",
            "tan skin",
            "brown skin",
            "deep brown skin",
            "freckled skin",
            "rosy complexion",
            "warm undertone",
            "cool undertone",
            "smooth skin",
            "textured skin",
            "weathered skin",
            "sun-kissed skin",
            "pale complexion",
        ],
        "Facial Details": [
            "dimples",
            "beauty mark",
            "scar across cheek",
            "small facial scar",
            "birthmark",
            "tattooed face markings",
            "painted face markings",
            "clean-shaven",
            "light stubble",
            "short beard",
            "full beard",
            "moustache",
            "defined nose",
            "soft nose",
            "full lips",
            "thin lips",
        ],
        "Presence": [
            "approachable presence",
            "commanding presence",
            "mysterious presence",
            "elegant presence",
            "rugged presence",
            "youthful appearance",
            "mature appearance",
            "tired appearance",
            "battle-worn appearance",
            "well-groomed appearance",
            "unkempt appearance",
            "otherworldly appearance",
        ],
    }
)

HAIR_OPTIONS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Length": [
            "shaved head",
            "buzz cut",
            "very short hair",
            "short hair",
            "chin-length hair",
            "shoulder-length hair",
            "long hair",
            "waist-length hair",
            "asymmetrical length",
            "shaved sides",
        ],
        "Texture and Shape": [
            "straight hair",
            "wavy hair",
            "curly hair",
            "coily hair",
            "afro-textured hair",
            "thick hair",
            "fine hair",
            "voluminous hair",
            "sleek hair",
            "messy hair",
            "wind-swept hair",
            "wet-look hair",
        ],
        "Style": [
            "side part",
            "middle part",
            "fringe",
            "curtain bangs",
            "pixie cut",
            "bob cut",
            "layered cut",
            "undercut",
            "mohawk",
            "slicked-back hair",
            "ponytail",
            "high ponytail",
            "low ponytail",
            "bun",
            "top knot",
            "braids",
            "box braids",
            "cornrows",
            "locs",
            "loose strands around face",
        ],
        "Colour": [
            "black hair",
            "dark brown hair",
            "brown hair",
            "chestnut hair",
            "auburn hair",
            "copper red hair",
            "ginger hair",
            "blonde hair",
            "platinum blonde hair",
            "silver hair",
            "grey hair",
            "white hair",
            "pastel pink hair",
            "blue hair",
            "green hair",
            "purple hair",
            "dyed streaks",
            "ombre colour",
        ],
        "Details": [
            "glossy hair",
            "matte hair",
            "braided crown",
            "decorative beads",
            "hair clips",
            "ribbon in hair",
            "metal hair ornament",
            "loose flyaway strands",
            "visible roots",
            "salt-and-pepper hair",
        ],
    }
)

EYES_OPTIONS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Colour": [
            "brown eyes",
            "dark brown eyes",
            "amber eyes",
            "hazel eyes",
            "green eyes",
            "blue eyes",
            "grey eyes",
            "violet eyes",
            "red stylised eyes",
            "heterochromia",
            "glowing eyes",
            "cybernetic eyes",
        ],
        "Shape and Structure": [
            "almond-shaped eyes",
            "round eyes",
            "hooded eyes",
            "monolid eyes",
            "deep-set eyes",
            "wide-set eyes",
            "narrow eyes",
            "large expressive eyes",
            "sharp intense eyes",
            "soft gentle eyes",
            "heavy eyelids",
            "tired eyes",
        ],
        "Brows and Expression": [
            "thick eyebrows",
            "thin eyebrows",
            "arched eyebrows",
            "straight eyebrows",
            "furrowed brow",
            "raised eyebrow",
            "focused gaze",
            "warm gaze",
            "piercing gaze",
            "dreamy gaze",
            "suspicious gaze",
            "wide-eyed look",
        ],
        "Makeup and Effects": [
            "subtle eyeliner",
            "bold eyeliner",
            "smoky eye makeup",
            "mascara",
            "bright eyeshadow",
            "dark eyeshadow",
            "tearful eyes",
            "dark circles under eyes",
            "strong catchlights",
            "reflected screen light in eyes",
            "sparkling eyes",
            "one eye covered",
        ],
    }
)

CLOTHING_OPTIONS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Tops": [
            "plain T-shirt",
            "graphic T-shirt",
            "tank top",
            "crop top",
            "button-up shirt",
            "collared shirt",
            "blouse",
            "tunic",
            "sweater",
            "hoodie",
            "vest",
            "tactical vest",
            "corset",
            "armour chestplate",
        ],
        "Outerwear": [
            "leather jacket",
            "denim jacket",
            "bomber jacket",
            "blazer",
            "trench coat",
            "long coat",
            "raincoat",
            "cloak",
            "cape",
            "hooded cloak",
            "lab coat",
            "robe",
            "space suit",
            "armoured suit",
        ],
        "Bottoms and Footwear": [
            "jeans",
            "cargo pants",
            "tailored trousers",
            "leggings",
            "skirt",
            "long skirt",
            "shorts",
            "utility belt",
            "layered fabrics",
            "combat boots",
            "ankle boots",
            "sneakers",
            "dress shoes",
            "sandals",
            "armoured boots",
            "barefoot",
        ],
        "Genre and Role": [
            "casual streetwear",
            "formal suit",
            "evening dress",
            "military uniform",
            "school uniform",
            "workwear",
            "sports kit",
            "fantasy adventurer outfit",
            "medieval attire",
            "Victorian-inspired attire",
            "gothic fashion",
            "cyberpunk fashion",
            "sci-fi pilot suit",
            "post-apocalyptic outfit",
            "ceremonial outfit",
            "royal outfit",
        ],
        "Material and Condition": [
            "cotton fabric",
            "linen fabric",
            "silk fabric",
            "wool fabric",
            "denim fabric",
            "leather material",
            "metal armour",
            "carbon-fibre panels",
            "reflective fabric",
            "glowing trim",
            "pristine clothing",
            "weathered clothing",
            "torn clothing",
            "dusty clothing",
            "wet clothing",
            "battle-worn clothing",
        ],
        "Colour Direction": [
            "black clothing",
            "white clothing",
            "grey clothing",
            "navy clothing",
            "crimson clothing",
            "emerald clothing",
            "gold accents",
            "silver accents",
            "earth-toned outfit",
            "pastel outfit",
            "high-visibility accents",
            "monochrome outfit",
            "contrasting colour blocks",
        ],
    }
)

ACCESSORY_OPTIONS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Wearables": [
            "glasses",
            "sunglasses",
            "goggles",
            "mask",
            "respirator",
            "helmet",
            "wide-brim hat",
            "baseball cap",
            "hood",
            "crown",
            "scarf",
            "gloves",
            "gauntlets",
            "belt",
            "harness",
            "backpack",
            "satchel",
        ],
        "Jewellery": [
            "earrings",
            "nose ring",
            "lip ring",
            "necklace",
            "pendant",
            "amulet",
            "rings",
            "bracelets",
            "wristwatch",
            "brooch",
            "hair ornament",
            "chain",
            "medallion",
            "beaded jewellery",
        ],
        "Tools and Props": [
            "book",
            "map",
            "lantern",
            "torch",
            "sword",
            "dagger",
            "staff",
            "wand",
            "bow",
            "shield",
            "camera",
            "phone",
            "tablet",
            "laptop",
            "compass",
            "key",
            "potion bottle",
            "medical kit",
            "musical instrument",
            "toolbox",
        ],
        "Tech and Effects": [
            "cybernetic arm",
            "cybernetic eye",
            "mechanical hand",
            "holographic display",
            "earpiece",
            "headphones",
            "jetpack",
            "drone companion",
            "glowing gem",
            "energy blade",
            "floating UI projection",
            "illuminated badge",
        ],
        "Small Details": [
            "worn leather straps",
            "metal buckles",
            "engraved metal",
            "stickers",
            "patches",
            "pins",
            "badges",
            "feathers",
            "charms",
            "wrapped bandages",
            "utility pouches",
            "paint splatters",
            "scratches and scuffs",
        ],
    }
)

SUBJECT_OPTION_GROUPS = {
    "appearance": APPEARANCE_OPTIONS,
    "hair": HAIR_OPTIONS,
    "eyes": EYES_OPTIONS,
    "clothing": CLOTHING_OPTIONS,
    "accessories": ACCESSORY_OPTIONS,
}

# type values: combo, line, multi, spin, check, file, position, options
SECTIONS: OrderedDict[str, list[tuple]] = OrderedDict(
    {
        "Image Setup": [
            ("image_type", "Image type", "combo", IMAGE_TYPES),
            ("purpose", "Purpose", "line", "Where and how the image will be used..."),
            ("aspect_ratio", "Aspect ratio", "combo", ASPECTS),
            ("orientation", "Orientation", "combo", [NS, "Portrait", "Landscape", "Square"]),
            ("monitor_position", "Monitor position", "position", MONITOR_POSITIONS),
            ("background_type", "Background", "combo", BACKGROUND_TYPES),
            (
                "framing",
                "Edge treatment",
                "combo",
                [
                    NS,
                    "Full bleed",
                    "Comfortable margin around subject",
                    "Print-safe margins",
                    "Keep all limbs and objects inside frame",
                ],
            ),
            ("safe_space", "Reserved empty space", "line", "Example: leave top-right empty for title text..."),
            ("variation_count", "Variations", "spin", (1, 12, 1)),
        ],
        "Subject": [
            ("subject_description", "Main subject", "multi", "Describe the subject in detail..."),
            ("subject_type", "Subject type", "combo", SUBJECT_TYPES),
            ("subject_count", "Subject count", "spin", (1, 50, 1)),
            ("age_range", "Age range", "combo", AGES),
            ("appearance", "Appearance", "options", SUBJECT_OPTION_GROUPS["appearance"]),
            ("hair", "Hair", "options", SUBJECT_OPTION_GROUPS["hair"]),
            ("eyes", "Eyes", "options", SUBJECT_OPTION_GROUPS["eyes"]),
            ("clothing", "Clothing", "options", SUBJECT_OPTION_GROUPS["clothing"]),
            ("accessories", "Accessories", "options", SUBJECT_OPTION_GROUPS["accessories"]),
            ("pose", "Pose", "combo", POSES),
            ("action", "Action", "line", "What exactly is happening..."),
            ("expression", "Expression", "combo", EXPRESSIONS),
            ("gaze", "Facing / gaze", "combo", GAZES),
        ],
        "Composition": [
            ("shot_type", "Shot type", "combo", SHOTS),
            ("camera_angle", "Camera angle", "combo", ANGLES),
            ("perspective", "Perspective / lens", "combo", PERSPECTIVES),
            ("subject_placement", "Subject placement", "combo", PLACEMENTS),
            ("depth_of_field", "Depth of field", "combo", DOF),
            ("visual_priority", "Visual priority", "line", "What should dominate the viewer's attention..."),
            ("composition_notes", "Extra notes", "multi", "Cropping, balance, leading lines, panel flow..."),
        ],
        "Environment": [
            ("location", "Location", "line", "Exact or imagined location..."),
            ("setting_type", "Setting type", "combo", SETTING_TYPES),
            ("time_period", "Time period", "combo", PERIODS),
            ("time_of_day", "Time of day", "combo", TIMES),
            ("weather", "Weather", "combo", WEATHER),
            (
                "architecture",
                "Architecture / materials",
                "multi",
                "Buildings, surfaces, construction style, textures...",
            ),
            (
                "background_elements",
                "Background elements",
                "multi",
                "Objects, people, signs, traffic, foliage, debris...",
            ),
            (
                "environment_condition",
                "Condition",
                "combo",
                [
                    NS,
                    "Clean and pristine",
                    "Lived-in",
                    "Crowded and busy",
                    "Abandoned",
                    "Damaged",
                    "Ruined",
                    "Luxurious",
                    "Minimalist",
                    "Dirty and gritty",
                    "Overgrown",
                ],
            ),
        ],
        "Lighting": [
            ("lighting_type", "Lighting type", "combo", LIGHTING),
            ("lighting_direction", "Direction", "combo", LIGHT_DIRECTIONS),
            ("colour_temperature", "Colour temperature", "combo", TEMPERATURES),
            ("contrast", "Contrast", "combo", CONTRASTS),
            ("atmosphere", "Atmospheric effects", "combo", ATMOSPHERES),
            (
                "lighting_notes",
                "Extra lighting notes",
                "multi",
                "Light sources, reflections, shadow behaviour...",
            ),
        ],
        "Art Style": [
            ("art_style", "Art style", "combo", ART_STYLES),
            ("linework", "Linework", "combo", LINEWORK),
            ("shading", "Shading", "combo", SHADING),
            ("detail_level", "Detail level", "combo", DETAIL),
            (
                "anatomy_style",
                "Anatomy / proportions",
                "combo",
                [
                    NS,
                    "Realistic anatomy",
                    "Slightly stylised anatomy",
                    "Heroic comic proportions",
                    "Exaggerated proportions",
                    "Chibi proportions",
                ],
            ),
            ("mood", "Mood", "combo", MOODS),
            (
                "style_notes",
                "Custom style direction",
                "multi",
                "Texture, era, visual language, print treatment, influences...",
            ),
        ],
        "Colour": [
            ("palette_style", "Palette style", "combo", PALETTES),
            ("main_colours", "Main colours", "line", "Colour names or HEX values..."),
            ("accent_colours", "Accent colours", "line", "Highlight colours or HEX values..."),
            ("saturation", "Saturation", "combo", SATURATION),
            ("colours_to_avoid", "Colours to avoid", "line", "Colours that must not appear..."),
            ("background_colour", "Background colour", "line", "Exact colour or HEX value..."),
        ],
        "Text": [
            (
                "exact_text",
                "Exact wording",
                "multi",
                "Enter exact text, including punctuation and capitalisation...",
            ),
            ("font_style", "Typography style", "combo", FONTS),
            ("text_placement", "Placement", "combo", TEXT_PLACEMENT),
            ("text_alignment", "Alignment", "combo", [NS, "Left aligned", "Centred", "Right aligned", "Justified"]),
            ("text_colour", "Text colour", "line", "Colour name or HEX value..."),
            ("text_notes", "Typography notes", "multi", "Hierarchy, outline, shadow, spacing..."),
        ],
        "Requirements": [
            ("must_include", "Must include", "multi", "One requirement per line..."),
            ("must_avoid", "Must avoid", "multi", "Objects, styles, defects, logos, crops, colours..."),
            (
                "continuity_notes",
                "Continuity notes",
                "multi",
                "Recurring character, outfit, location, prop, scale...",
            ),
            (
                "unchanged_details",
                "Keep unchanged",
                "multi",
                "For edits: identity, pose, lighting, costume, layout...",
            ),
            ("reference_image", "Reference image", "file", ""),
            (
                "editing_changes",
                "Requested changes",
                "multi",
                "Remove, add, replace, extend, recolour, repair, enhance...",
            ),
        ],
        "Output Options": [
            (
                "additional_versions",
                "Additional versions",
                "multi",
                "Day/night, with/without text, alternate pose, transparent version...",
            ),
            (
                "output_finish",
                "Final finish",
                "combo",
                [
                    NS,
                    "Production-ready final artwork",
                    "Clean concept exploration",
                    "Rough exploratory draft",
                    "Print-ready finish",
                    "Web-ready finish",
                    "Transparent asset-ready finish",
                ],
            ),
            ("quality_safeguards", "Quality safeguards", "check", True),
            ("text_warning", "Typography warning", "check", True),
        ],
    }
)


class ComboCustomField(QWidget):
    def __init__(self, options: list[str]) -> None:
        super().__init__()
        self.combo = QComboBox()
        self.combo.addItems(options)
        self.custom = QLineEdit()
        self.custom.setPlaceholderText("Custom or additional detail...")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.combo, 1)
        layout.addWidget(self.custom, 2)

    def value(self) -> str:
        selected = self.combo.currentText().strip()
        custom = self.custom.text().strip()
        if selected in {NS, "None", "No text"}:
            selected = ""
        if selected and custom:
            return f"{selected}; additional detail: {custom}"
        return selected or custom

    def data(self) -> dict[str, str]:
        return {"selected": self.combo.currentText(), "custom": self.custom.text()}

    def set_data(self, value: Any) -> None:
        if isinstance(value, dict):
            selected = str(value.get("selected", NS))
            custom = str(value.get("custom", ""))
        else:
            selected, custom = str(value or NS), ""
        index = self.combo.findText(selected)
        if index < 0:
            index, custom = 0, selected
        self.combo.setCurrentIndex(index)
        self.custom.setText(custom)

    def clear(self) -> None:
        self.combo.setCurrentIndex(0)
        self.custom.clear()

    def randomise(self) -> None:
        if self.combo.count() > 1:
            self.combo.setCurrentIndex(random.randrange(1, self.combo.count()))


class MonitorPositionDialog(QDialog):
    def __init__(self, options: list[tuple[str, str]], selected_value: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Select monitor position")
        self.setMinimumWidth(520)
        self.options = options
        self.selected_value = selected_value
        self.buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Pick where the subject or focal point should sit on the image frame."))

        monitor = QGroupBox("Monitor")
        grid = QGridLayout(monitor)
        for index, (label, value) in enumerate(options):
            row, column = divmod(index, 3)
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumSize(130, 64)
            button.clicked.connect(lambda _checked=False, option=value: self.select_position(option))
            grid.addWidget(button, row, column)
            self.buttons[value] = button
        layout.addWidget(monitor)

        clear_button = QPushButton("Clear selection")
        clear_button.clicked.connect(self.clear_selection)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        bottom = QHBoxLayout()
        bottom.addWidget(clear_button)
        bottom.addStretch(1)
        bottom.addWidget(button_box)
        layout.addLayout(bottom)

        if selected_value:
            self.select_position(selected_value)

    def select_position(self, value: str) -> None:
        self.selected_value = value
        for option, button in self.buttons.items():
            button.setChecked(option == value)

    def clear_selection(self) -> None:
        self.selected_value = ""
        for button in self.buttons.values():
            button.setChecked(False)

    def value(self) -> str:
        return self.selected_value


class MonitorPositionField(QWidget):
    def __init__(self, options: list[tuple[str, str]]) -> None:
        super().__init__()
        self.options = options
        self.selected = ""

        self.summary = QLineEdit()
        self.summary.setReadOnly(True)
        self.summary.setPlaceholderText("Pick a position on the monitor...")

        choose_button = QPushButton("Pick")
        choose_button.clicked.connect(self.open_picker)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.summary, 1)
        layout.addWidget(choose_button)
        layout.addWidget(clear_button)

    def refresh(self) -> None:
        label = next((label for label, value in self.options if value == self.selected), "")
        self.summary.setText(label)

    def open_picker(self) -> None:
        dialog = MonitorPositionDialog(self.options, self.selected, self)
        if dialog.exec() == QDialog.Accepted:
            self.selected = dialog.value()
            self.refresh()

    def value(self) -> str:
        return self.selected

    def data(self) -> str:
        return self.selected

    def set_data(self, value: Any) -> None:
        self.selected = str(value or "")
        valid_values = {option_value for _label, option_value in self.options}
        if self.selected not in valid_values:
            self.selected = ""
        self.refresh()

    def clear(self) -> None:
        self.selected = ""
        self.refresh()


class OptionPickerDialog(QDialog):
    def __init__(
        self,
        title: str,
        groups: OrderedDict[str, list[str]],
        selected: list[str],
        custom_notes: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Choose {title.lower()} options")
        self.resize(760, 620)
        self.checkboxes: dict[str, QCheckBox] = {}

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select as many options as apply. Add custom notes only when the checklist is not enough."))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        selected_set = set(selected)
        for group_name, options in groups.items():
            box = QGroupBox(group_name)
            grid = QGridLayout(box)
            for index, option in enumerate(options):
                checkbox = QCheckBox(option)
                checkbox.setChecked(option in selected_set)
                row, column = divmod(index, 2)
                grid.addWidget(checkbox, row, column)
                self.checkboxes[option] = checkbox
            content_layout.addWidget(box)
        content_layout.addStretch(1)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        self.custom = QPlainTextEdit()
        self.custom.setPlaceholderText("Optional custom notes...")
        self.custom.setPlainText(custom_notes)
        self.custom.setMaximumHeight(90)
        layout.addWidget(QLabel("Custom notes"))
        layout.addWidget(self.custom)

        clear_button = QPushButton("Clear checks")
        clear_button.clicked.connect(self.clear_checks)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        bottom = QHBoxLayout()
        bottom.addWidget(clear_button)
        bottom.addStretch(1)
        bottom.addWidget(button_box)
        layout.addLayout(bottom)

    def selected_values(self) -> list[str]:
        return [option for option, checkbox in self.checkboxes.items() if checkbox.isChecked()]

    def custom_text(self) -> str:
        return self.custom.toPlainText().strip()

    def clear_checks(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)


class OptionPickerField(QWidget):
    def __init__(self, label: str, groups: OrderedDict[str, list[str]]) -> None:
        super().__init__()
        self.label = label
        self.groups = groups
        self.option_order = [option for options in groups.values() for option in options]
        self.selected: list[str] = []
        self.custom_notes = ""

        self.summary = QPlainTextEdit()
        self.summary.setReadOnly(True)
        self.summary.setPlaceholderText("Use Choose options to fill this without typing...")
        self.summary.setMinimumHeight(72)
        self.summary.setMaximumHeight(108)

        choose_button = QPushButton("Choose options")
        choose_button.clicked.connect(self.open_picker)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        buttons = QHBoxLayout()
        buttons.addWidget(choose_button)
        buttons.addWidget(clear_button)
        buttons.addStretch(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.summary)
        layout.addLayout(buttons)

    def value(self) -> str:
        selected_text = ", ".join(self.selected)
        if selected_text and self.custom_notes:
            return f"{selected_text}; additional detail: {self.custom_notes}"
        return selected_text or self.custom_notes

    def data(self) -> dict[str, Any]:
        return {"selected": self.selected, "custom": self.custom_notes}

    def set_data(self, value: Any) -> None:
        if isinstance(value, dict):
            selected = value.get("selected", [])
            if isinstance(selected, str):
                selected_items = self.parse_items(selected)
            elif isinstance(selected, list):
                selected_items = [str(item).strip() for item in selected if str(item).strip()]
            else:
                selected_items = []
            self.selected = self.normalise_selected(selected_items)
            self.custom_notes = str(value.get("custom", "") or "").strip()
        else:
            text = str(value or "").strip()
            selected_items = self.parse_items(text)
            self.selected = self.normalise_selected(selected_items)
            if self.selected:
                known = set(self.selected)
                leftovers = [item for item in selected_items if item not in known]
                self.custom_notes = ", ".join(leftovers)
            else:
                self.custom_notes = text
        self.refresh()

    def open_picker(self) -> None:
        dialog = OptionPickerDialog(self.label, self.groups, self.selected, self.custom_notes, self)
        if dialog.exec() == QDialog.Accepted:
            self.selected = self.normalise_selected(dialog.selected_values())
            self.custom_notes = dialog.custom_text()
            self.refresh()

    def refresh(self) -> None:
        self.summary.setPlainText(self.value())

    def clear(self) -> None:
        self.selected = []
        self.custom_notes = ""
        self.refresh()

    def normalise_selected(self, values: list[str]) -> list[str]:
        selected_set = set(values)
        return [option for option in self.option_order if option in selected_set]

    @staticmethod
    def parse_items(text: str) -> list[str]:
        for marker in ["; additional detail:", "; Additional detail:", "additional detail:"]:
            text = text.replace(marker, ",")
        separators_normalised = text.replace("\n", ",").replace(";", ",")
        return [item.strip() for item in separators_normalised.split(",") if item.strip()]


class FileField(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Optional reference image path...")
        button = QPushButton("Browse")
        button.clicked.connect(self.browse)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit, 1)
        layout.addWidget(button)

    def browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select reference image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp);;All files (*.*)",
        )
        if path:
            self.edit.setText(path)

    def value(self) -> str:
        return self.edit.text().strip()

    def data(self) -> str:
        return self.edit.text()

    def set_data(self, value: Any) -> None:
        self.edit.setText(str(value or ""))

    def clear(self) -> None:
        self.edit.clear()


class ImagePromptBuilder(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings(ORG_NAME, APP_NAME)
        self.widgets: dict[str, QWidget] = {}
        self.labels: dict[str, str] = {}
        self.outputs: OrderedDict[str, QPlainTextEdit] = OrderedDict()

        self.setWindowTitle(APP_NAME)
        self.resize(1420, 900)
        self.setMinimumSize(1050, 700)
        self.build_ui()
        self.restore_window()

    def build_ui(self) -> None:
        self.build_toolbar()
        root_widget = QWidget()
        root = QVBoxLayout(root_widget)

        project_box = QGroupBox("Project")
        project_form = QFormLayout(project_box)
        self.mode = QComboBox()
        self.mode.addItems(
            [
                "New image",
                "Edit existing image",
                "Character sheet",
                "Comic panel",
                "Comic page",
                "Poster or cover",
                "Logo or UI element",
                "Environment concept",
                "Object or vehicle concept",
            ]
        )
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Optional project, scene, character, or asset name...")
        self.recent = QComboBox()
        self.recent.currentIndexChanged.connect(self.load_recent)
        project_form.addRow("Mode", self.mode)
        project_form.addRow("Project name", self.project_name)
        project_form.addRow("Recent prompt", self.recent)
        root.addWidget(project_box)

        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)

        self.input_tabs = QTabWidget()
        for section, definitions in SECTIONS.items():
            self.add_section_tab(section, definitions)
        splitter.addWidget(self.input_tabs)

        self.output_tabs = QTabWidget()
        for key, title in [
            ("full", "Full Prompt"),
            ("structured", "Structured"),
            ("negative", "Negative Prompt"),
            ("editing", "Editing Instructions"),
            ("continuity", "Continuity Summary"),
            ("compact", "Compact Prompt"),
        ]:
            editor = QPlainTextEdit()
            editor.setPlaceholderText(f"{title} will appear here...")
            self.outputs[key] = editor
            self.output_tabs.addTab(editor, title)
        splitter.addWidget(self.output_tabs)
        splitter.setSizes([560, 300])
        root.addWidget(splitter, 1)

        buttons = QHBoxLayout()
        for text, slot in [
            ("Generate Prompts", self.generate),
            ("Copy Active Tab", self.copy_active),
            ("Save Output TXT", self.save_output),
        ]:
            button = QPushButton(text)
            button.clicked.connect(slot)
            buttons.addWidget(button)
        buttons.addStretch(1)
        random_button = QPushButton("Randomise Dropdowns")
        random_button.clicked.connect(self.randomise)
        clear_button = QPushButton("Clear Form")
        clear_button.clicked.connect(self.clear_form)
        buttons.addWidget(random_button)
        buttons.addWidget(clear_button)
        root.addLayout(buttons)

        self.setCentralWidget(root_widget)
        self.refresh_recent()
        self.statusBar().showMessage("Ready")

        QShortcut(QKeySequence("Ctrl+Return"), self, activated=self.generate)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, activated=self.copy_active)

    def build_toolbar(self) -> None:
        toolbar = QToolBar("Files")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        for text, shortcut, slot in [
            ("Save Preset", QKeySequence.Save, self.save_preset),
            ("Load Preset", QKeySequence.Open, self.load_preset),
            ("Export JSON", None, self.export_json),
            ("Import JSON", None, self.load_preset),
        ]:
            action = QAction(text, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(slot)
            toolbar.addAction(action)

    def add_section_tab(self, section: str, definitions: list[tuple]) -> None:
        page = QWidget()
        outer = QVBoxLayout(page)
        content = QWidget()
        form = QFormLayout(content)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignTop)

        for key, label, field_type, config in definitions:
            widget = self.make_field(field_type, config, label)
            self.widgets[key] = widget
            self.labels[key] = label
            form.addRow(label if field_type != "check" else "", widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(content)
        outer.addWidget(scroll)
        self.input_tabs.addTab(page, section)

    @staticmethod
    def make_field(field_type: str, config: Any, label: str) -> QWidget:
        if field_type == "combo":
            return ComboCustomField(config)
        if field_type == "line":
            widget = QLineEdit()
            widget.setPlaceholderText(config)
            return widget
        if field_type == "multi":
            widget = QPlainTextEdit()
            widget.setPlaceholderText(config)
            widget.setMinimumHeight(86)
            widget.setMaximumHeight(135)
            return widget
        if field_type == "spin":
            minimum, maximum, default = config
            widget = QSpinBox()
            widget.setRange(minimum, maximum)
            widget.setValue(default)
            return widget
        if field_type == "check":
            widget = QCheckBox(label)
            widget.setChecked(bool(config))
            return widget
        if field_type == "file":
            return FileField()
        if field_type == "position":
            return MonitorPositionField(config)
        if field_type == "options":
            return OptionPickerField(label, config)
        raise ValueError(f"Unknown field type: {field_type}")

    def widget_value(self, widget: QWidget) -> Any:
        if isinstance(widget, (ComboCustomField, FileField, MonitorPositionField, OptionPickerField)):
            return widget.value()
        if isinstance(widget, QLineEdit):
            return widget.text().strip()
        if isinstance(widget, QPlainTextEdit):
            return widget.toPlainText().strip()
        if isinstance(widget, QSpinBox):
            return widget.value()
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        return ""

    def widget_data(self, widget: QWidget) -> Any:
        if isinstance(widget, (ComboCustomField, FileField, MonitorPositionField, OptionPickerField)):
            return widget.data()
        if isinstance(widget, QLineEdit):
            return widget.text()
        if isinstance(widget, QPlainTextEdit):
            return widget.toPlainText()
        if isinstance(widget, QSpinBox):
            return widget.value()
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        return None

    def set_widget_data(self, widget: QWidget, value: Any) -> None:
        if isinstance(widget, (ComboCustomField, FileField, MonitorPositionField, OptionPickerField)):
            widget.set_data(value)
        elif isinstance(widget, QLineEdit):
            widget.setText(str(value or ""))
        elif isinstance(widget, QPlainTextEdit):
            widget.setPlainText(str(value or ""))
        elif isinstance(widget, QSpinBox):
            try:
                widget.setValue(int(value))
            except (TypeError, ValueError):
                pass
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))

    def values(self) -> dict[str, Any]:
        return {key: self.widget_value(widget) for key, widget in self.widgets.items()}

    def preset_data(self, include_outputs: bool = True) -> dict[str, Any]:
        data = {
            "preset_version": PRESET_VERSION,
            "mode": self.mode.currentText(),
            "project_name": self.project_name.text(),
            "fields": {key: self.widget_data(widget) for key, widget in self.widgets.items()},
        }
        if include_outputs:
            data["outputs"] = {key: editor.toPlainText() for key, editor in self.outputs.items()}
        return data

    @staticmethod
    def clean(value: Any) -> str:
        if value is None or isinstance(value, bool):
            return ""
        text = str(value).strip()
        return "" if text in {"", NS, "None", "No text"} else text

    @staticmethod
    def list_items(text: str) -> list[str]:
        return [
            line.strip(" -\t")
            for line in text.replace(";", "\n").splitlines()
            if line.strip(" -\t")
        ]

    def generate(self) -> None:
        v = self.values()
        project = self.project_name.text().strip()
        mode = self.mode.currentText()

        section_blocks: list[str] = []
        structured = [f"MODE: {mode}"]
        if project:
            structured.append(f"PROJECT: {project}")

        for section, definitions in SECTIONS.items():
            lines = []
            for key, label, _field_type, _config in definitions:
                value = v.get(key)
                if isinstance(value, bool):
                    continue
                cleaned = self.clean(value)
                if cleaned:
                    lines.append(f"{label}: {cleaned}")
            if lines:
                section_blocks.append(section.upper() + "\n" + "\n".join(lines))
                structured.extend(["", section.upper() + ":", *[f"- {line}" for line in lines]])

        image_type = self.clean(v.get("image_type")) or "image"
        purpose = self.clean(v.get("purpose"))
        intro = f"Create a {image_type.lower()}"
        if project:
            intro += f' for "{project}"'
        if purpose:
            intro += f", intended for {purpose}"
        intro += f". Generation mode: {mode}."

        full = intro + "\n\n" + "\n\n".join(section_blocks)
        exact_text = self.clean(v.get("exact_text"))
        if exact_text and bool(v.get("text_warning")):
            full += (
                "\n\nTYPOGRAPHY NOTE\n"
                "Prioritise exact spelling and clean placement. For critical production text, "
                "final lettering may be added separately during layout."
            )

        negatives = self.list_items(self.clean(v.get("must_avoid")))
        avoid_colours = self.clean(v.get("colours_to_avoid"))
        if avoid_colours:
            negatives.append(f"unwanted colours: {avoid_colours}")
        if bool(v.get("quality_safeguards")):
            negatives += [
                "extra fingers",
                "missing fingers",
                "extra limbs",
                "duplicated limbs",
                "malformed hands",
                "warped anatomy",
                "distorted face",
                "duplicated subjects",
                "unintended cropping",
                "cut-off feet",
                "accidental text",
                "watermarks",
                "unrequested logos",
                "low resolution",
                "heavy blur",
                "compression artifacts",
            ]
        negatives = list(dict.fromkeys(negatives))
        negative = ", ".join(negatives) or "No negative prompt requirements specified."

        editing = self.make_editing(v, mode, project)
        continuity = self.make_continuity(v, project)
        compact = self.make_compact(v, mode, project)

        for key, text in {
            "full": full.strip(),
            "structured": "\n".join(structured).strip(),
            "negative": negative,
            "editing": editing,
            "continuity": continuity,
            "compact": compact,
        }.items():
            self.outputs[key].setPlainText(text)

        self.add_recent(full.strip())
        self.statusBar().showMessage("Prompts generated", 4000)

    def make_editing(self, v: dict[str, Any], mode: str, project: str) -> str:
        reference = self.clean(v.get("reference_image")) or "Not selected"
        changes = self.clean(v.get("editing_changes")) or "No edit-specific changes entered."
        unchanged = self.clean(v.get("unchanged_details")) or "Preserve all areas not explicitly mentioned."
        continuity = self.clean(v.get("continuity_notes"))
        lines = [f"MODE: {mode}"]
        if project:
            lines.append(f"ASSET: {project}")
        lines += [
            f"REFERENCE IMAGE: {reference}",
            "",
            "CHANGES TO MAKE:",
            changes,
            "",
            "KEEP UNCHANGED:",
            unchanged,
            "",
            "MATCHING REQUIREMENTS:",
            "Match the original perspective, scale, lighting, shadows, reflections, texture, and image grain where applicable.",
        ]
        if continuity:
            lines += ["", "CONTINUITY RULES:", continuity]
        return "\n".join(lines)

    def make_continuity(self, v: dict[str, Any], project: str) -> str:
        lines = [f"PROJECT / ASSET: {project}"] if project else []
        for key, heading in [
            ("subject_description", "CORE SUBJECT"),
            ("appearance", "APPEARANCE"),
            ("hair", "HAIR"),
            ("eyes", "EYES"),
            ("clothing", "CLOTHING"),
            ("accessories", "ACCESSORIES / PROPS"),
            ("continuity_notes", "CONTINUITY RULES"),
            ("unchanged_details", "LOCKED DETAILS"),
            ("reference_image", "REFERENCE IMAGE"),
        ]:
            value = self.clean(v.get(key))
            if value:
                lines += ["", f"{heading}:", value]
        return "\n".join(lines).strip() or "No continuity information entered."

    def make_compact(self, v: dict[str, Any], mode: str, project: str) -> str:
        parts = [f"Mode: {mode}"]
        if project:
            parts.append(f"Project: {project}")
        priority = [
            "image_type",
            "subject_description",
            "appearance",
            "hair",
            "eyes",
            "clothing",
            "accessories",
            "pose",
            "action",
            "expression",
            "shot_type",
            "camera_angle",
            "location",
            "time_of_day",
            "weather",
            "lighting_type",
            "lighting_direction",
            "art_style",
            "linework",
            "shading",
            "mood",
            "palette_style",
            "main_colours",
            "aspect_ratio",
            "monitor_position",
            "background_type",
            "must_include",
            "must_avoid",
        ]
        for key in priority:
            value = self.clean(v.get(key))
            if value:
                parts.append(f"{self.labels[key]}: {value.replace(chr(10), '; ')}")
        return " | ".join(parts)

    def copy_active(self) -> None:
        editor = self.outputs[list(self.outputs)[self.output_tabs.currentIndex()]]
        text = editor.toPlainText().strip()
        if not text:
            QMessageBox.information(self, APP_NAME, "The active output tab is empty.")
            return
        QApplication.clipboard().setText(text)
        self.statusBar().showMessage("Copied to clipboard", 3500)

    def save_output(self) -> None:
        key = list(self.outputs)[self.output_tabs.currentIndex()]
        text = self.outputs[key].toPlainText().strip()
        if not text:
            QMessageBox.information(self, APP_NAME, "The active output tab is empty.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save output",
            self.suggest_name(key, ".txt"),
            "Text files (*.txt)",
        )
        if path:
            try:
                Path(path).write_text(text, encoding="utf-8")
                self.statusBar().showMessage(f"Saved {path}", 5000)
            except OSError as exc:
                QMessageBox.critical(self, APP_NAME, f"Could not save file:\n{exc}")

    def save_preset(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save preset",
            self.suggest_name("preset", ".json"),
            "JSON files (*.json)",
        )
        if path:
            self.write_json(path, self.preset_data(True))

    def export_json(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            self.suggest_name("image_prompt", ".json"),
            "JSON files (*.json)",
        )
        if path:
            data = self.preset_data(True)
            data["generated_values"] = self.values()
            self.write_json(path, data)

    def load_preset(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load preset",
            "",
            "JSON files (*.json);;All files (*.*)",
        )
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object.")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not load file:\n{exc}")
            return

        mode_index = self.mode.findText(str(data.get("mode", "New image")))
        self.mode.setCurrentIndex(max(0, mode_index))
        self.project_name.setText(str(data.get("project_name", "")))
        for key, value in data.get("fields", {}).items():
            if key in self.widgets:
                self.set_widget_data(self.widgets[key], value)
        for key, value in data.get("outputs", {}).items():
            if key in self.outputs:
                self.outputs[key].setPlainText(str(value or ""))
        self.statusBar().showMessage(f"Loaded {path}", 5000)

    def write_json(self, path: str, data: dict[str, Any]) -> None:
        try:
            Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            self.statusBar().showMessage(f"Saved {path}", 5000)
        except (OSError, TypeError) as exc:
            QMessageBox.critical(self, APP_NAME, f"Could not save file:\n{exc}")

    def suggest_name(self, suffix: str, extension: str) -> str:
        name = self.project_name.text().strip() or "image_prompt"
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name).strip("_")
        return f"{safe or 'image_prompt'}_{suffix}{extension}"

    def randomise(self) -> None:
        for widget in self.widgets.values():
            if isinstance(widget, ComboCustomField):
                widget.randomise()
        self.statusBar().showMessage("Dropdowns randomised", 3000)

    def clear_form(self) -> None:
        answer = QMessageBox.question(
            self,
            APP_NAME,
            "Clear all inputs and outputs?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        self.mode.setCurrentIndex(0)
        self.project_name.clear()
        for key, widget in self.widgets.items():
            if isinstance(widget, (ComboCustomField, FileField, MonitorPositionField, OptionPickerField)):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QPlainTextEdit):
                widget.clear()
            elif isinstance(widget, QSpinBox):
                widget.setValue(1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(key in {"quality_safeguards", "text_warning"})
        for editor in self.outputs.values():
            editor.clear()
        self.statusBar().showMessage("Form cleared", 3000)

    def recent_prompts(self) -> list[str]:
        value = self.settings.value("recent_prompts", [])
        if isinstance(value, str):
            return [value] if value else []
        return [str(item) for item in value] if isinstance(value, list) else []

    def add_recent(self, prompt: str) -> None:
        recent = [item for item in self.recent_prompts() if item != prompt]
        recent.insert(0, prompt)
        self.settings.setValue("recent_prompts", recent[:15])
        self.refresh_recent()

    def refresh_recent(self) -> None:
        self.recent.blockSignals(True)
        self.recent.clear()
        self.recent.addItem("Select a recent generated prompt...")
        for prompt in self.recent_prompts():
            label = " ".join(prompt.split())
            self.recent.addItem(label[:110] + ("..." if len(label) > 110 else ""), prompt)
        self.recent.setCurrentIndex(0)
        self.recent.blockSignals(False)

    def load_recent(self, index: int) -> None:
        if index > 0:
            self.outputs["full"].setPlainText(str(self.recent.itemData(index)))
            self.output_tabs.setCurrentIndex(0)

    def restore_window(self) -> None:
        geometry = self.settings.value("geometry")
        state = self.settings.value("window_state")
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("window_state", self.saveState())
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    app.setStyle("Fusion")
    window = ImagePromptBuilder()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
