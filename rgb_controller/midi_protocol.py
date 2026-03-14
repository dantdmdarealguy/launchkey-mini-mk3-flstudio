"""
MIDI protocol constants and color palette for the Novation Launchkey Mini MK3.

Lighting Protocol Summary
=========================
The Launchkey Mini MK3 uses standard 3-byte MIDI messages for LED control:

  STATUS  DATA1  DATA2
  ------  -----  -----
  0x90    note   color   -> Pad solid/static color
  0x92    note   color   -> Pad pulsing color
  0xB0    cc     color   -> Button solid/static color
  0xB2    cc     color   -> Button pulsing color

- DATA1 identifies the specific pad or button (note number or CC number).
- DATA2 is the color index (0-127) from the Novation 128-color palette.
- Color 0 turns the LED off.

DAW Mode Activation
===================
  Status 159 (0x9F), Channel 0, Data1 12, Data2 127  -> Enter DAW mode
  Status 159 (0x9F), Channel 0, Data1 12, Data2 0    -> Exit DAW mode

Pad Note Numbers (Session Mode)
================================
  Upper row: 96-103  (0x60-0x67)
  Lower row: 112-119 (0x70-0x77)

Button CC Numbers
=================
  Play:       CC 115 (0x73)
  Record:     CC 117 (0x75)
  Scene Up:   CC 104 (0x68)
  Scene Down:  CC 105 (0x69)
  Scene Left:  CC 103 (0x67)  -- arrow left / track left
  Scene Right: CC 102 (0x66)  -- arrow right / track right
"""

# ---------------------------------------------------------------------------
# 128-Color Palette (index -> RGB tuple)
# Reverse-engineered from the FL Studio MIDI script's ``colPalette.py`` which
# stores the same Novation colour table used across Launchkey / Launchpad
# devices.  See ``colPalette.palette`` in the repository root.
# ---------------------------------------------------------------------------
PALETTE = [
    (97, 97, 97),       # 0   Grey
    (179, 179, 179),    # 1   Light Grey
    (221, 221, 221),    # 2   White
    (255, 255, 255),    # 3   Bright White
    (255, 179, 179),    # 4   Pink
    (255, 97, 97),      # 5   Bright Pink
    (221, 97, 97),      # 6   Red
    (179, 97, 97),      # 7   Dark Red
    (255, 243, 213),    # 8   Peach
    (255, 179, 97),     # 9   Orange
    (221, 140, 97),     # 10  Dark Orange
    (179, 118, 97),     # 11  Brown
    (255, 238, 161),    # 12  Yellow
    (255, 255, 97),     # 13  Bright Yellow
    (221, 221, 97),     # 14  Lime
    (179, 179, 97),     # 15  Dark Lime
    (221, 255, 161),    # 16  Green
    (194, 255, 97),     # 17  Bright Green
    (161, 221, 97),     # 18  Light Green
    (129, 179, 97),     # 19  Dark Green
    (194, 255, 179),    # 20  Turquoise
    (97, 255, 97),      # 21  Bright Turquoise
    (97, 221, 97),      # 22
    (97, 179, 97),      # 23
    (194, 255, 194),    # 24
    (97, 255, 140),     # 25
    (97, 221, 118),     # 26
    (97, 179, 107),     # 27
    (194, 255, 204),    # 28
    (97, 255, 204),     # 29
    (97, 221, 161),     # 30
    (97, 179, 129),     # 31
    (194, 255, 243),    # 32
    (97, 255, 233),     # 33
    (97, 221, 194),     # 34
    (97, 179, 150),     # 35
    (194, 243, 255),    # 36
    (97, 238, 255),     # 37
    (97, 199, 221),     # 38
    (97, 161, 179),     # 39
    (194, 221, 255),    # 40
    (97, 199, 255),     # 41
    (97, 161, 221),     # 42
    (97, 129, 179),     # 43
    (161, 140, 255),    # 44
    (97, 97, 255),      # 45
    (97, 97, 221),      # 46
    (97, 97, 179),      # 47
    (204, 179, 255),    # 48
    (161, 97, 255),     # 49
    (129, 97, 221),     # 50
    (118, 97, 179),     # 51
    (255, 179, 255),    # 52
    (255, 97, 255),     # 53
    (221, 97, 221),     # 54
    (179, 97, 179),     # 55
    (255, 179, 213),    # 56
    (255, 97, 194),     # 57
    (221, 97, 161),     # 58
    (179, 97, 140),     # 59
    (255, 118, 97),     # 60
    (233, 179, 97),     # 61
    (221, 194, 97),     # 62
    (161, 161, 97),     # 63
    (97, 179, 97),      # 64
    (97, 179, 140),     # 65
    (97, 140, 213),     # 66
    (97, 97, 255),      # 67
    (97, 179, 179),     # 68
    (140, 97, 243),     # 69
    (204, 179, 194),    # 70
    (140, 118, 129),    # 71
    (255, 97, 97),      # 72
    (243, 255, 161),    # 73
    (238, 252, 97),     # 74
    (204, 255, 97),     # 75
    (118, 221, 97),     # 76
    (97, 255, 204),     # 77
    (97, 233, 255),     # 78
    (97, 161, 255),     # 79
    (140, 97, 255),     # 80
    (204, 97, 252),     # 81
    (238, 140, 221),    # 82
    (161, 118, 97),     # 83
    (255, 161, 97),     # 84
    (221, 249, 97),     # 85
    (213, 255, 140),    # 86
    (97, 255, 97),      # 87
    (179, 255, 161),    # 88
    (204, 252, 213),    # 89
    (179, 255, 246),    # 90
    (204, 228, 255),    # 91
    (161, 194, 246),    # 92
    (213, 194, 249),    # 93
    (249, 140, 255),    # 94
    (255, 97, 204),     # 95
    (255, 194, 97),     # 96
    (243, 238, 97),     # 97
    (228, 255, 97),     # 98
    (221, 204, 97),     # 99
    (179, 161, 97),     # 100
    (97, 186, 118),     # 101
    (118, 194, 140),    # 102
    (129, 129, 161),    # 103
    (129, 140, 204),    # 104
    (204, 170, 129),    # 105
    (221, 97, 97),      # 106
    (249, 179, 161),    # 107
    (249, 186, 118),    # 108
    (255, 243, 140),    # 109
    (233, 249, 161),    # 110
    (213, 238, 118),    # 111
    (255, 255, 255),    # 112
    (249, 249, 213),    # 113
    (221, 252, 228),    # 114
    (233, 233, 255),    # 115
    (228, 213, 255),    # 116
    (179, 179, 179),    # 117
    (213, 213, 213),    # 118
    (249, 255, 255),    # 119
    (233, 97, 97),      # 120
    (170, 97, 97),      # 121
    (129, 246, 97),     # 122
    (97, 179, 97),      # 123
    (243, 238, 97),     # 124
    (179, 161, 97),     # 125
    (238, 194, 97),     # 126
    (194, 118, 97),     # 127
]

# ---------------------------------------------------------------------------
# Pad layout – Session mode note numbers (the mode used in DAW mode)
# ---------------------------------------------------------------------------
# Upper row pads 1-8
SESSION_UPPER_PADS = list(range(96, 104))   # 0x60 .. 0x67
# Lower row pads 9-16
SESSION_LOWER_PADS = list(range(112, 120))  # 0x70 .. 0x77
# All 16 pads in visual order (top-left to bottom-right)
ALL_PADS = SESSION_UPPER_PADS + SESSION_LOWER_PADS

# Human-readable labels (1-indexed, matching the physical layout)
PAD_LABELS = {note: f"Pad {i+1}" for i, note in enumerate(ALL_PADS)}

# ---------------------------------------------------------------------------
# Navigation / transport button CC numbers
# ---------------------------------------------------------------------------
BUTTON_SCENE_UP = 104    # 0x68
BUTTON_SCENE_DOWN = 105  # 0x69
BUTTON_TRACK_LEFT = 103  # 0x67
BUTTON_TRACK_RIGHT = 102 # 0x66

ALL_BUTTONS = [
    BUTTON_TRACK_LEFT,
    BUTTON_TRACK_RIGHT,
    BUTTON_SCENE_UP,
    BUTTON_SCENE_DOWN,
]

BUTTON_LABELS = {
    BUTTON_TRACK_LEFT: "◀ Track",
    BUTTON_TRACK_RIGHT: "Track ▶",
    BUTTON_SCENE_UP: "▲ Scene",
    BUTTON_SCENE_DOWN: "Scene ▼",
}

# ---------------------------------------------------------------------------
# MIDI status bytes for lighting
# ---------------------------------------------------------------------------
PAD_STATIC = 0x90    # Note On, channel 1 – solid color
PAD_PULSE = 0x92     # Note On, channel 3 – pulsing color
BUTTON_STATIC = 0xB0 # CC, channel 1 – solid color
BUTTON_PULSE = 0xB2  # CC, channel 3 – pulsing color

# DAW mode activation
DAW_MODE_STATUS = 0x9F   # 159
DAW_MODE_DATA1 = 0x0C    # 12
DAW_MODE_ON = 127
DAW_MODE_OFF = 0

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rgb_to_palette_index(r: int, g: int, b: int) -> int:
    """Find the closest palette color to the given RGB value using weighted
    Euclidean distance (matching the algorithm from the original FL Studio script)."""
    best_index = 0
    best_dist = float("inf")
    for i, (pr, pg, pb) in enumerate(PALETTE):
        dist = 0.3 * (r - pr) ** 2 + 0.6 * (g - pg) ** 2 + 0.1 * (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_index = i
    return best_index


def palette_index_to_hex(index: int) -> str:
    """Return an HTML hex color string for a palette index."""
    r, g, b = PALETTE[index]
    return f"#{r:02x}{g:02x}{b:02x}"
