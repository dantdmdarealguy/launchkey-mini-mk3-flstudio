"""Tests for rgb_controller.midi_protocol."""

import unittest
import sys
import os

# Ensure the repo root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from rgb_controller.midi_protocol import (
    PALETTE,
    ALL_PADS,
    SESSION_UPPER_PADS,
    SESSION_LOWER_PADS,
    ALL_BUTTONS,
    BUTTON_SCENE_UP,
    BUTTON_SCENE_DOWN,
    BUTTON_TRACK_LEFT,
    BUTTON_TRACK_RIGHT,
    PAD_STATIC,
    PAD_PULSE,
    BUTTON_STATIC,
    BUTTON_PULSE,
    rgb_to_palette_index,
    palette_index_to_hex,
)


class TestPalette(unittest.TestCase):
    def test_palette_length(self):
        self.assertEqual(len(PALETTE), 128)

    def test_palette_entries_are_rgb_tuples(self):
        for idx, entry in enumerate(PALETTE):
            self.assertEqual(len(entry), 3, f"Palette entry {idx} is not a 3-tuple")
            for component in entry:
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)

    def test_palette_index_0_is_grey(self):
        self.assertEqual(PALETTE[0], (97, 97, 97))

    def test_palette_index_3_is_bright_white(self):
        self.assertEqual(PALETTE[3], (255, 255, 255))

    def test_palette_index_5_is_bright_red(self):
        self.assertEqual(PALETTE[5], (255, 97, 97))


class TestPadLayout(unittest.TestCase):
    def test_upper_pads_notes(self):
        self.assertEqual(SESSION_UPPER_PADS, [96, 97, 98, 99, 100, 101, 102, 103])

    def test_lower_pads_notes(self):
        self.assertEqual(SESSION_LOWER_PADS, [112, 113, 114, 115, 116, 117, 118, 119])

    def test_all_pads_count(self):
        self.assertEqual(len(ALL_PADS), 16)


class TestButtons(unittest.TestCase):
    def test_button_cc_numbers(self):
        self.assertEqual(BUTTON_SCENE_UP, 104)
        self.assertEqual(BUTTON_SCENE_DOWN, 105)
        self.assertEqual(BUTTON_TRACK_LEFT, 103)
        self.assertEqual(BUTTON_TRACK_RIGHT, 102)

    def test_all_buttons_count(self):
        self.assertEqual(len(ALL_BUTTONS), 4)


class TestStatusBytes(unittest.TestCase):
    def test_pad_static(self):
        self.assertEqual(PAD_STATIC, 0x90)

    def test_pad_pulse(self):
        self.assertEqual(PAD_PULSE, 0x92)

    def test_button_static(self):
        self.assertEqual(BUTTON_STATIC, 0xB0)

    def test_button_pulse(self):
        self.assertEqual(BUTTON_PULSE, 0xB2)


class TestColorConversion(unittest.TestCase):
    def test_exact_match_red(self):
        # Palette index 5 is (255, 97, 97)
        self.assertEqual(rgb_to_palette_index(255, 97, 97), 5)

    def test_exact_match_white(self):
        self.assertEqual(rgb_to_palette_index(255, 255, 255), 3)

    def test_pure_red_maps_to_reddish(self):
        idx = rgb_to_palette_index(255, 0, 0)
        r, g, b = PALETTE[idx]
        self.assertGreater(r, g)
        self.assertGreater(r, b)

    def test_pure_blue_maps_to_bluish(self):
        idx = rgb_to_palette_index(0, 0, 255)
        r, g, b = PALETTE[idx]
        self.assertGreaterEqual(b, r)

    def test_palette_index_to_hex(self):
        self.assertEqual(palette_index_to_hex(0), "#616161")
        self.assertEqual(palette_index_to_hex(3), "#ffffff")


class TestPresets(unittest.TestCase):
    def test_presets_loadable(self):
        from rgb_controller.presets import PRESETS
        self.assertGreater(len(PRESETS), 0)

    def test_all_preset_pad_targets_valid(self):
        from rgb_controller.presets import PRESETS
        for preset in PRESETS:
            for pc in preset.pad_colors:
                self.assertIn(pc.target, ALL_PADS,
                              f"Preset '{preset.name}' has invalid pad target {pc.target}")
                self.assertGreaterEqual(pc.color_index, 0)
                self.assertLessEqual(pc.color_index, 127)

    def test_all_preset_button_targets_valid(self):
        from rgb_controller.presets import PRESETS
        for preset in PRESETS:
            for bc in preset.button_colors:
                self.assertIn(bc.target, ALL_BUTTONS,
                              f"Preset '{preset.name}' has invalid button target {bc.target}")
                self.assertGreaterEqual(bc.color_index, 0)
                self.assertLessEqual(bc.color_index, 127)


if __name__ == "__main__":
    unittest.main()
