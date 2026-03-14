"""
CustomTkinter GUI for the Launchkey Mini MK3 RGB Controller.

The window mirrors the physical layout of the controller and provides:
- Clickable pads that open a color picker
- Navigation buttons with color control
- A preset selector panel
- MIDI port connection management
"""

from __future__ import annotations

import tkinter as tk
from tkinter import colorchooser

import customtkinter as ctk

from . import midi_protocol as proto
from .midi_interface import LaunchkeyMini, find_launchkey_port
from .presets import PRESETS

# ---------------------------------------------------------------------------
# Application constants
# ---------------------------------------------------------------------------
PAD_SIZE = 64
PAD_GAP = 6
BUTTON_WIDTH = 72
BUTTON_HEIGHT = 32


def _rgb_tuple_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Main application window
# ---------------------------------------------------------------------------

class RGBControllerApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Launchkey Mini MK3 — RGB Controller")
        self.resizable(False, False)

        # MIDI device
        self._lk = LaunchkeyMini()

        # Track current color index for each pad / button
        self._pad_colors: dict[int, int] = {n: 0 for n in proto.ALL_PADS}
        self._btn_colors: dict[int, int] = {cc: 0 for cc in proto.ALL_BUTTONS}

        # Keep references to GUI pad widgets so we can update them
        self._pad_widgets: dict[int, ctk.CTkButton] = {}
        self._btn_widgets: dict[int, ctk.CTkButton] = {}

        # Build the UI
        self._build_connection_bar()
        self._build_controller_panel()
        self._build_preset_panel()
        self._build_status_bar()

        # Try auto-connecting
        self._auto_connect()

    # -- UI construction ----------------------------------------------------

    def _build_connection_bar(self) -> None:
        frame = ctk.CTkFrame(self, corner_radius=0)
        frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(frame, text="MIDI Port:").pack(side="left", padx=(8, 4))

        self._port_var = ctk.StringVar(value="(not connected)")
        self._port_menu = ctk.CTkOptionMenu(
            frame,
            variable=self._port_var,
            values=self._available_ports(),
            width=280,
        )
        self._port_menu.pack(side="left", padx=4)

        self._refresh_btn = ctk.CTkButton(
            frame, text="↻ Refresh", width=80, command=self._refresh_ports
        )
        self._refresh_btn.pack(side="left", padx=4)

        self._connect_btn = ctk.CTkButton(
            frame, text="Connect", width=80, command=self._toggle_connection
        )
        self._connect_btn.pack(side="left", padx=4)

        self._daw_var = ctk.BooleanVar(value=True)
        self._daw_check = ctk.CTkCheckBox(
            frame, text="DAW Mode", variable=self._daw_var
        )
        self._daw_check.pack(side="left", padx=(12, 8))

    def _build_controller_panel(self) -> None:
        """Build the visual representation of the controller."""
        outer = ctk.CTkFrame(self)
        outer.pack(padx=10, pady=10)

        # --- Navigation buttons (above the pad grid) ---
        nav_frame = ctk.CTkFrame(outer, fg_color="transparent")
        nav_frame.pack(pady=(4, 2))

        for cc in proto.ALL_BUTTONS:
            label = proto.BUTTON_LABELS[cc]
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                fg_color="#333333",
                hover_color="#555555",
                corner_radius=6,
                command=lambda c=cc: self._on_button_click(c),
            )
            btn.pack(side="left", padx=3)
            self._btn_widgets[cc] = btn

        # --- 16 drum pads (2 rows of 8) ---
        pad_frame = ctk.CTkFrame(outer, fg_color="transparent")
        pad_frame.pack(pady=4)

        for row_idx, row_notes in enumerate(
            [proto.SESSION_UPPER_PADS, proto.SESSION_LOWER_PADS]
        ):
            for col_idx, note in enumerate(row_notes):
                btn = ctk.CTkButton(
                    pad_frame,
                    text="",
                    width=PAD_SIZE,
                    height=PAD_SIZE,
                    fg_color="#444444",
                    hover_color="#666666",
                    corner_radius=8,
                    command=lambda n=note: self._on_pad_click(n),
                )
                btn.grid(row=row_idx, column=col_idx, padx=PAD_GAP // 2, pady=PAD_GAP // 2)
                self._pad_widgets[note] = btn

    def _build_preset_panel(self) -> None:
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=10, pady=(0, 4))

        ctk.CTkLabel(frame, text="RGB Presets:", font=ctk.CTkFont(size=13, weight="bold")).pack(
            side="left", padx=(8, 6)
        )

        for preset in PRESETS:
            b = ctk.CTkButton(
                frame,
                text=preset.name,
                width=80,
                height=28,
                command=lambda p=preset: self._apply_preset(p),
            )
            b.pack(side="left", padx=3, pady=6)

    def _build_status_bar(self) -> None:
        self._status_var = ctk.StringVar(value="Ready")
        bar = ctk.CTkLabel(
            self,
            textvariable=self._status_var,
            font=ctk.CTkFont(size=11),
            anchor="w",
        )
        bar.pack(fill="x", padx=14, pady=(0, 8))

    # -- port helpers -------------------------------------------------------

    @staticmethod
    def _available_ports() -> list[str]:
        import mido
        try:
            ports = mido.get_output_names()
        except Exception:
            ports = []
        return ports if ports else ["(no ports found)"]

    def _refresh_ports(self) -> None:
        ports = self._available_ports()
        self._port_menu.configure(values=ports)
        if ports:
            self._port_var.set(ports[0])
        self._set_status("Port list refreshed")

    def _auto_connect(self) -> None:
        port = find_launchkey_port()
        if port:
            self._port_var.set(port)
            self._do_connect(port)
        else:
            self._set_status("No Launchkey Mini detected — select a port manually")

    def _toggle_connection(self) -> None:
        if self._lk.is_connected:
            self._do_disconnect()
        else:
            self._do_connect(self._port_var.get())

    def _do_connect(self, port_name: str) -> None:
        try:
            self._lk.connect(port_name)
        except Exception as exc:
            self._set_status(f"Connection failed: {exc}")
            return
        if self._daw_var.get():
            self._lk.enter_daw_mode()
        self._connect_btn.configure(text="Disconnect")
        self._set_status(f"Connected to {port_name}")

    def _do_disconnect(self) -> None:
        self._lk.disconnect()
        self._connect_btn.configure(text="Connect")
        self._set_status("Disconnected")

    # -- pad / button interaction -------------------------------------------

    def _on_pad_click(self, note: int) -> None:
        """Open a color picker and apply the chosen color to a pad."""
        color_index = self._pick_color(self._pad_colors.get(note, 0))
        if color_index is not None:
            self._set_pad(note, color_index)

    def _on_button_click(self, cc: int) -> None:
        """Open a color picker for a nav button."""
        color_index = self._pick_color(self._btn_colors.get(cc, 0))
        if color_index is not None:
            self._set_button(cc, color_index)

    def _pick_color(self, current_index: int) -> int | None:
        """Show the palette picker dialog and return the chosen palette index,
        or *None* if cancelled."""
        dialog = PaletteDialog(self, current_index)
        self.wait_window(dialog)
        return dialog.result

    # -- set colors ---------------------------------------------------------

    def _set_pad(self, note: int, color_index: int, *, pulse: bool = False) -> None:
        self._pad_colors[note] = color_index
        r, g, b = proto.PALETTE[color_index]
        hex_color = _rgb_tuple_to_hex(r, g, b)
        widget = self._pad_widgets.get(note)
        if widget:
            widget.configure(fg_color=hex_color)
        self._lk.set_pad_color(note, color_index, pulse=pulse)

    def _set_button(self, cc: int, color_index: int, *, pulse: bool = False) -> None:
        self._btn_colors[cc] = color_index
        r, g, b = proto.PALETTE[color_index]
        hex_color = _rgb_tuple_to_hex(r, g, b)
        widget = self._btn_widgets.get(cc)
        if widget:
            widget.configure(fg_color=hex_color)
        self._lk.set_button_color(cc, color_index, pulse=pulse)

    # -- presets ------------------------------------------------------------

    def _apply_preset(self, preset) -> None:
        for pc in preset.pad_colors:
            self._set_pad(pc.target, pc.color_index, pulse=pc.pulse)
        for bc in preset.button_colors:
            self._set_button(bc.target, bc.color_index, pulse=bc.pulse)
        self._set_status(f"Preset applied: {preset.name}")

    # -- status -------------------------------------------------------------

    def _set_status(self, msg: str) -> None:
        self._status_var.set(msg)


# ---------------------------------------------------------------------------
# Palette picker dialog
# ---------------------------------------------------------------------------

class PaletteDialog(ctk.CTkToplevel):
    """A modal dialog showing the 128-color Novation palette as clickable
    swatches.  Also includes a system color-picker button that finds the
    closest palette match."""

    def __init__(self, parent: ctk.CTk, current_index: int = 0) -> None:
        super().__init__(parent)
        self.title("Choose a Pad Color")
        self.resizable(False, False)
        self.grab_set()
        self.result: int | None = None

        # Palette grid (16 columns × 8 rows = 128 swatches)
        grid = ctk.CTkFrame(self)
        grid.pack(padx=10, pady=10)

        for idx in range(128):
            r, g, b = proto.PALETTE[idx]
            hex_c = _rgb_tuple_to_hex(r, g, b)
            row, col = divmod(idx, 16)
            border_width = 2 if idx == current_index else 0
            btn = tk.Button(
                grid,
                bg=hex_c,
                activebackground=hex_c,
                width=2,
                height=1,
                relief="solid" if idx == current_index else "flat",
                borderwidth=border_width,
                command=lambda i=idx: self._select(i),
            )
            btn.grid(row=row, column=col, padx=1, pady=1)

        # Bottom bar
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            bottom, text="Custom Color…", width=120, command=self._custom_color
        ).pack(side="left")

        ctk.CTkButton(
            bottom, text="Off (0)", width=60, command=lambda: self._select(0)
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            bottom, text="Cancel", width=60, command=self.destroy
        ).pack(side="right")

    def _select(self, index: int) -> None:
        self.result = index
        self.destroy()

    def _custom_color(self) -> None:
        rgb, _ = colorchooser.askcolor(title="Pick a color")
        if rgb is not None:
            r, g, b = (int(c) for c in rgb)
            idx = proto.rgb_to_palette_index(r, g, b)
            self._select(idx)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run() -> None:
    app = RGBControllerApp()
    app.mainloop()
