# Launchkey Mini MK3 — Standalone RGB Controller

A standalone Python application that controls the RGB LEDs on the **Novation Launchkey Mini MK3** without requiring FL Studio or any DAW.

## MIDI Lighting Protocol Summary

The Launchkey Mini MK3 uses standard 3-byte MIDI messages for LED control:

| STATUS | DATA1 | DATA2 | Effect |
|--------|-------|-------|--------|
| `0x90` | pad note | color 0-127 | Pad — solid/static color |
| `0x92` | pad note | color 0-127 | Pad — pulsing color |
| `0xB0` | button CC | color 0-127 | Button — solid/static color |
| `0xB2` | button CC | color 0-127 | Button — pulsing color |

- **DATA1** identifies the specific pad or button.
- **DATA2** is the color index (0–127) from the Novation 128-color palette.
- Color index **0** turns the LED off.

### DAW Mode Activation
The device must be placed in DAW mode to accept LED commands:
```
Status 0x9F, Data1 12, Data2 127  →  Enter DAW mode
Status 0x9F, Data1 12, Data2 0    →  Exit DAW mode
```

### Pad Note Numbers (Session/DAW Mode)
| Pad | Upper Row | Lower Row |
|-----|-----------|-----------|
| 1   | 96        | 112       |
| 2   | 97        | 113       |
| 3   | 98        | 114       |
| 4   | 99        | 115       |
| 5   | 100       | 116       |
| 6   | 101       | 117       |
| 7   | 102       | 118       |
| 8   | 103       | 119       |

### Navigation Button CC Numbers
| Button | CC Number |
|--------|-----------|
| Track Left (◀) | 103 |
| Track Right (▶) | 102 |
| Scene Up (▲) | 104 |
| Scene Down (▼) | 105 |

## Installation

```bash
pip install -r rgb_controller/requirements.txt
```

### Dependencies
- **mido** ≥ 1.3.0 — MIDI message handling
- **python-rtmidi** ≥ 1.5.0 — Cross-platform MIDI I/O backend
- **customtkinter** ≥ 5.2.0 — Modern GUI framework

## Usage

```bash
python -m rgb_controller
```

The application will:
1. Auto-detect the Launchkey Mini MK3 MIDI output port
2. Enter DAW mode (if the checkbox is enabled)
3. Display a visual layout mirroring the controller's 16 pads and 4 navigation buttons
4. Let you click any pad/button to open a 128-color palette picker
5. Provide built-in presets (Rainbow, Vaporwave, Fire, Ocean, etc.)

## Project Structure

```
rgb_controller/
├── __init__.py          # Package marker
├── __main__.py          # Entry point (python -m rgb_controller)
├── midi_protocol.py     # Color palette, pad/button mappings, MIDI constants
├── midi_interface.py    # mido/rtmidi MIDI output wrapper
├── gui.py               # CustomTkinter GUI application
├── presets.py           # Built-in RGB lighting presets
├── requirements.txt     # Python dependencies
└── tests/
    ├── __init__.py
    └── test_protocol.py # Unit tests for protocol and presets
```
