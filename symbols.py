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
    should be an SVG path definition that fits in a `FONT_SIZE`-sided square
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
        path="M320,-80 Q303,-80,291.5,-91.5 T280,-120 V-760"
        "Q280,-777,291.5,-788.5 T320,-800 H400 V-880 H560 V-800 H640"
        "Q657,-800,668.5,-788.5 T680,-760 V-120 Q680,-103,668.5,-91.5 T640,-80 H320 Z"
        "M360,-160 H600 V-720 H360 V-160 Z",
        variants={
            100: "M320,-80 Q303,-80,291.5,-91.5 T280,-120 V-760"
            "Q280,-777,291.5,-788.5 T320,-800 H400 V-880 H560 V-800 H640"
            "Q657,-800,668.5,-788.5 T680,-760 V-120"
            "Q680,-103,668.5,-91.5 T640,-80 H320 Z"
            "M360,-720 H600 V-720 H360 V-720 Z"
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
        path="M80,-80 L880,-880 V-80 H80 Z M800,-160 V-686 L273,-160 V-160 H800 Z",
        variants={
            100: "M80,-80 L880,-880 V-80 H80 Z M800,-160 V-686 H800 V-160 H800 Z"
        },
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
