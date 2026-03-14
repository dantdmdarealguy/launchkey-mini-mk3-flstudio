"""
MIDI interface for the Novation Launchkey Mini MK3.

Replaces FL Studio's ``device.midiOutMsg`` with standard ``mido`` / ``python-rtmidi``
calls so the lighting logic can run standalone.
"""

from __future__ import annotations

import mido
import mido.backends.rtmidi  # noqa: F401 – ensure the rtmidi backend is loaded

from . import midi_protocol as proto


# ---------------------------------------------------------------------------
# Port discovery
# ---------------------------------------------------------------------------

_LAUNCHKEY_KEYWORDS = ["launchkey mini", "launchkey mini mk3", "lkmk3"]


def _can_list_ports() -> bool:
    """Return True if the MIDI backend can enumerate ports."""
    try:
        mido.get_output_names()
        return True
    except Exception:
        return False


def find_launchkey_port() -> str | None:
    """Return the name of the first MIDI output port whose name contains a
    Launchkey Mini keyword (case-insensitive), or *None* if no match is found.

    The Launchkey Mini MK3 typically exposes two MIDI ports.  The one labelled
    "MIDIIN2" / "MIDIOUT2" (or "LK Mini MK3 MIDI" on macOS) is the DAW port.
    We prefer a port whose name includes "MIDI" but *not* "DAW" — which is the
    standard MIDI port required for DAW-mode LED control.
    """
    available = mido.get_output_names() if _can_list_ports() else []
    # First pass: look for a DAW port explicitly
    for name in available:
        lower = name.lower()
        if any(kw in lower for kw in _LAUNCHKEY_KEYWORDS):
            if "midi" in lower or "daw" in lower:
                return name
    # Second pass: accept any match
    for name in available:
        lower = name.lower()
        if any(kw in lower for kw in _LAUNCHKEY_KEYWORDS):
            return name
    return None


# ---------------------------------------------------------------------------
# Controller class
# ---------------------------------------------------------------------------

class LaunchkeyMini:
    """Thin wrapper around a ``mido`` output port that speaks the Launchkey
    Mini MK3 lighting protocol."""

    def __init__(self, port_name: str | None = None) -> None:
        self._port: mido.ports.BaseOutput | None = None
        self._port_name = port_name

    # -- connection ---------------------------------------------------------

    @property
    def is_connected(self) -> bool:
        return self._port is not None and not self._port.closed

    def connect(self, port_name: str | None = None) -> None:
        """Open the MIDI output port.  If *port_name* is ``None`` the port is
        auto-detected."""
        name = port_name or self._port_name or find_launchkey_port()
        if name is None:
            raise RuntimeError(
                "No Launchkey Mini MK3 detected.  Available ports: "
                + ", ".join(mido.get_output_names())
            )
        self._port = mido.open_output(name)
        self._port_name = name

    def disconnect(self) -> None:
        if self._port is not None and not self._port.closed:
            self.exit_daw_mode()
            self._port.close()
        self._port = None

    # -- raw send -----------------------------------------------------------

    def _send(self, status: int, data1: int, data2: int) -> None:
        """Send a raw 3-byte MIDI message exactly like
        ``device.midiOutMsg(status, 0, data1, data2)`` did in the FL Studio
        script.  The channel nibble is already encoded in *status*."""
        if self._port is None:
            return
        self._port.send(mido.Message.from_bytes([status, data1 & 0x7F, data2 & 0x7F]))

    # -- DAW mode -----------------------------------------------------------

    def enter_daw_mode(self) -> None:
        self._send(proto.DAW_MODE_STATUS, proto.DAW_MODE_DATA1, proto.DAW_MODE_ON)

    def exit_daw_mode(self) -> None:
        self._send(proto.DAW_MODE_STATUS, proto.DAW_MODE_DATA1, proto.DAW_MODE_OFF)

    # -- pad lighting -------------------------------------------------------

    def set_pad_color(self, note: int, color_index: int, *, pulse: bool = False) -> None:
        """Set a pad LED to a palette color.

        Parameters
        ----------
        note : int
            The MIDI note number of the pad (see ``midi_protocol.ALL_PADS``).
        color_index : int
            Palette index 0-127.
        pulse : bool
            If *True* the LED will pulse; otherwise it stays solid.
        """
        status = proto.PAD_PULSE if pulse else proto.PAD_STATIC
        self._send(status, note, color_index)

    # -- button lighting ----------------------------------------------------

    def set_button_color(self, cc: int, color_index: int, *, pulse: bool = False) -> None:
        """Set a navigation button LED to a palette color.

        Parameters
        ----------
        cc : int
            The CC number (see ``midi_protocol.ALL_BUTTONS``).
        color_index : int
            Palette index 0-127.
        pulse : bool
            If *True* the LED will pulse; otherwise it stays solid.
        """
        status = proto.BUTTON_PULSE if pulse else proto.BUTTON_STATIC
        self._send(status, cc, color_index)

    # -- convenience --------------------------------------------------------

    def all_off(self) -> None:
        """Turn off every controllable LED."""
        for note in proto.ALL_PADS:
            self.set_pad_color(note, 0)
        for cc in proto.ALL_BUTTONS:
            self.set_button_color(cc, 0)

    def set_all_pads(self, color_index: int, *, pulse: bool = False) -> None:
        for note in proto.ALL_PADS:
            self.set_pad_color(note, color_index, pulse=pulse)

    def set_all_buttons(self, color_index: int, *, pulse: bool = False) -> None:
        for cc in proto.ALL_BUTTONS:
            self.set_button_color(cc, color_index, pulse=pulse)
