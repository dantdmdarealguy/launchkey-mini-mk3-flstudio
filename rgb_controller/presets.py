"""Built-in RGB presets for the Launchkey Mini MK3 RGB Controller."""

from __future__ import annotations

from typing import NamedTuple

from . import midi_protocol as proto


class PadColor(NamedTuple):
    """Color assignment for a single pad or button."""
    target: int       # note number (pad) or CC number (button)
    color_index: int  # palette index 0-127
    pulse: bool       # True = pulsing, False = solid


class Preset(NamedTuple):
    """A named lighting preset."""
    name: str
    description: str
    pad_colors: list[PadColor]
    button_colors: list[PadColor]


def _all_pads(color: int, pulse: bool = False) -> list[PadColor]:
    return [PadColor(n, color, pulse) for n in proto.ALL_PADS]


def _all_buttons(color: int, pulse: bool = False) -> list[PadColor]:
    return [PadColor(cc, color, pulse) for cc in proto.ALL_BUTTONS]


def _rainbow_pads() -> list[PadColor]:
    """Assign a rainbow spread across the 16 pads."""
    rainbow = [5, 9, 13, 17, 21, 37, 41, 45, 49, 53, 57, 60, 84, 96, 72, 80]
    return [PadColor(n, rainbow[i], False) for i, n in enumerate(proto.ALL_PADS)]


def _vaporwave_pads() -> list[PadColor]:
    """Pastel pink / purple / cyan aesthetic."""
    colors = [52, 56, 48, 44, 36, 40, 48, 52, 56, 52, 48, 44, 36, 40, 48, 56]
    return [PadColor(n, colors[i], False) for i, n in enumerate(proto.ALL_PADS)]


def _fire_pads() -> list[PadColor]:
    """Red-orange-yellow gradient (fire effect)."""
    colors = [5, 5, 60, 60, 9, 9, 84, 84, 13, 13, 96, 96, 12, 12, 8, 8]
    return [PadColor(n, colors[i], False) for i, n in enumerate(proto.ALL_PADS)]


def _ocean_pads() -> list[PadColor]:
    """Blue-cyan-teal gradient."""
    colors = [45, 46, 42, 41, 37, 38, 34, 33, 78, 79, 66, 67, 45, 46, 42, 41]
    return [PadColor(n, colors[i], False) for i, n in enumerate(proto.ALL_PADS)]


def _pulse_party_pads() -> list[PadColor]:
    """Colorful pulsing pads for a party look."""
    colors = [5, 9, 13, 21, 37, 45, 49, 53, 57, 60, 72, 80, 84, 96, 17, 41]
    return [PadColor(n, colors[i], True) for i, n in enumerate(proto.ALL_PADS)]


def _matrix_pads() -> list[PadColor]:
    """Green hacker / matrix theme."""
    greens = [21, 22, 23, 19, 76, 87, 122, 123, 18, 64, 101, 102, 25, 26, 27, 17]
    return [PadColor(n, greens[i], False) for i, n in enumerate(proto.ALL_PADS)]


# ---------------------------------------------------------------------------
# Preset registry
# ---------------------------------------------------------------------------

PRESETS: list[Preset] = [
    Preset(
        name="All Off",
        description="Turn off all LEDs",
        pad_colors=_all_pads(0),
        button_colors=_all_buttons(0),
    ),
    Preset(
        name="All Red",
        description="All pads bright red",
        pad_colors=_all_pads(5),
        button_colors=_all_buttons(5),
    ),
    Preset(
        name="All Green",
        description="All pads bright green",
        pad_colors=_all_pads(21),
        button_colors=_all_buttons(21),
    ),
    Preset(
        name="All Blue",
        description="All pads bright blue",
        pad_colors=_all_pads(45),
        button_colors=_all_buttons(45),
    ),
    Preset(
        name="All White",
        description="All pads bright white",
        pad_colors=_all_pads(3),
        button_colors=_all_buttons(3),
    ),
    Preset(
        name="Rainbow",
        description="Rainbow spread across pads",
        pad_colors=_rainbow_pads(),
        button_colors=[
            PadColor(proto.BUTTON_TRACK_LEFT, 5, False),
            PadColor(proto.BUTTON_TRACK_RIGHT, 45, False),
            PadColor(proto.BUTTON_SCENE_UP, 21, False),
            PadColor(proto.BUTTON_SCENE_DOWN, 53, False),
        ],
    ),
    Preset(
        name="Vaporwave",
        description="Pastel pink, purple & cyan aesthetic",
        pad_colors=_vaporwave_pads(),
        button_colors=_all_buttons(52),
    ),
    Preset(
        name="Fire",
        description="Red-orange-yellow gradient",
        pad_colors=_fire_pads(),
        button_colors=_all_buttons(9),
    ),
    Preset(
        name="Ocean",
        description="Blue-cyan-teal gradient",
        pad_colors=_ocean_pads(),
        button_colors=_all_buttons(41),
    ),
    Preset(
        name="Pulse Party",
        description="Colorful pulsing pads",
        pad_colors=_pulse_party_pads(),
        button_colors=_all_buttons(53, pulse=True),
    ),
    Preset(
        name="Matrix",
        description="Green hacker theme",
        pad_colors=_matrix_pads(),
        button_colors=_all_buttons(21),
    ),
]
