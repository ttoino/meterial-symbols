"""Defines the different symbols available in the font."""

from dataclasses import dataclass


@dataclass
class Symbol:
    """Represents a symbol available in the font."""

    name: str
    """Internal symbol name, not shown to the user"""
    path: str
    """
    The default glyph for this symbol;
    should be an SVG path definition that fits in an `ICON_SIZE`-sided square
    """
    variants: dict[int, str]
    """
    The different variants for this symbol; the keys represent a point in our axis,
    and the values should be a path with same constraints as `path`
    """
    characters: set[str | int]
    """
    The characters that map to this symbol; `int`s represent unicode code-points,
    strings represent ligatures (currently not supported by `fonttools`)
    """


SYMBOLS: list[Symbol] = [
    Symbol(
        name="battery",
        path="M17,5v16c0,0.55-0.45,1-1,1H8c-0.55,0-1-0.45-1-1V5"
        "c0-0.55,0.45-1,1-1h2V2h4v2h2C16.55,4,17,4.45,17,5z"
        "M15,6H9v14h6V6z",
        variants={
            100: "M17,5v16c0,0.55-0.45,1-1,1H8c-0.55,0-1-0.45-1-1V5"
            "c0-0.55,0.45-1,1-1h2V2h4v2h2C16.55,4,17,4.45,17,5z"
            "M15,6H9v0h6V6z"
        },
        characters={
            0xFF000,
            "battery",
            0xE1A4,
            "battery_full",
            0xEBDC,
            "battery_0_bar",
            0xEBD9,
            "battery_1_bar",
            0xEBE0,
            "battery_2_bar",
            0xEBDD,
            "battery_3_bar",
            0xEBE2,
            "battery_4_bar",
            0xEBD4,
            "battery_5_bar",
            0xEBD2,
            "battery_6_bar",
        },
    ),
    Symbol(
        name="network_cell",
        path="M2,22h20V2L2,22z M20,20H6.83v0L20,6.83z",
        variants={100: "M2,22h20V2L2,22z M20,20h0V6.83L20,6.83z"},
        characters={
            0xFF001,
            0xE1B9,
            "network_cell",
            0xF0A8,
            "signal_cellular_0_bar",
            0xF0A9,
            "signal_cellular_1_bar",
            0xF0AA,
            "signal_cellular_2_bar",
            0xF0AB,
            "signal_cellular_3_bar",
            0xE1C8,
            "signal_cellular_4_bar",
            0xE1CF,
            "signal_cellular_null",
        },
    ),
]
"""All the symbols the font supplies; order is significant and should not change"""
