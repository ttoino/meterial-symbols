"""Generates the font."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, config
from fontTools.designspaceLib import AxisDescriptor
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.transform import Identity
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import SVGPath
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables.TupleVariation import TupleVariation

NAME = "Meterial Symbols"
"""The font name"""
SAFE_NAME = re.sub(r"\W", "", NAME)
STYLE = "Regular"
"""The font style"""
VERSION = "1.0.0"
"""The font version"""
AUTHOR = "Toino"
"""The font author"""

FONT_SIZE = 960
"""The size of a character in font units, equivalent to `unitsPerEm`"""
ASCENT = 1056
"""The size of a character ascent"""
DESCENT = -96
"""The size of a character descent"""

AXIS_TAG = "PGRS"
"""The tag for our custom axis, should be four capitalized letters"""
AXIS_NAME = "Progress"
"""Human readable name for our custom axis"""
AXIS_MIN = 0
"""Minimum user supplied value for our custom axis"""
AXIS_MAX = 100
"""Maximum user supplied value for our custom axis"""
AXIS_DEFAULT = 0
"""Default user supplied value for our custom axis"""


@dataclass
class Symbol(DataClassJsonMixin):
    """Represents a symbol available in the font."""

    name: str
    """Internal symbol name, not shown to the user"""
    codepoints: set[int] = field(
        metadata=config(decoder=lambda x: {int(i, 16) for i in x})
    )
    """
    The unicode codepoints that map to this symbol
    """
    ligatures: set[str]
    """
    The ligature strings that map to this symbol
    """


def glyph_from_svg(svg_path: Path) -> Glyph:
    """Generate a glyph from an SVG path."""
    svg = SVGPath(
        svg_path,
        # SVG coordinates are mirrored on the Y-axis
        Identity.scale(1, -1),
    )

    ttpen = TTGlyphPen()
    svg.draw(ttpen)

    return ttpen.glyph()


def tuple_variations(
    base: Glyph, variations: dict[float, Glyph]
) -> list[TupleVariation]:
    """Generate tuple variations from the base glyph, coordinates, and paths."""
    # We should only provide the needed deltas,
    # if we provide deltas for all points the font breaks (no idea why).
    # If we provide points only for points that change,
    # neighboring points also get interpolated,
    # so we should also provide deltas for these neighbors.

    variations_list = sorted(variations.items())
    gvar: list[TupleVariation] = []

    for i, (coord, glyph) in enumerate(variations_list):
        last = 0
        selected: set[int] = set()

        for j in range(glyph.numberOfContours):
            for k in range(last, glyph.endPtsOfContours[j] + 1):
                if glyph.coordinates[k] != base.coordinates[k]:
                    selected |= {
                        # Previous point
                        k - 1 if k > last else glyph.endPtsOfContours[j],
                        k,
                        # Next point
                        k + 1 if k < glyph.endPtsOfContours[j] else last,
                    }

            last = glyph.endPtsOfContours[j] + 1

        prev = 0 if i == 0 else variations_list[i - 1][0]
        nxt = 1 if i == len(variations) - 1 else variations_list[i + 1][0]

        gvar.append(
            TupleVariation(
                {AXIS_TAG: (prev, coord, nxt)},
                [
                    (
                        glyph.coordinates[i][0] - base.coordinates[i][0],
                        glyph.coordinates[i][1] - base.coordinates[i][1],
                    )
                    if i in selected
                    else None
                    for i in range(len(glyph.coordinates))
                ],
            )
        )

    return gvar


def main() -> None:
    """Generate the font."""
    with Path("symbols.json").open(encoding="utf-8") as f:
        symbols = Symbol.schema().loads(f.read(), many=True)

    glyph_order = [""]
    char_map: dict[int, str] = {}
    glyphs = {"": Glyph()}
    g_var: dict[str, list[TupleVariation]] = {}
    h_metrics = {"": (0, 0)}

    for symbol in symbols:
        base_path = Path(f"symbols/{symbol.name}")

        glyph_order.append(symbol.name)

        char_map |= {
            code: symbol.name for code in symbol.codepoints if isinstance(code, int)
        }

        glyph = glyph_from_svg(base_path / "_.svg")
        glyph.recalcBounds(None)
        glyphs[symbol.name] = glyph

        variants = {
            float(svg.stem): glyph_from_svg(svg)
            for svg in base_path.glob("*.svg")
            if svg.stem != "_"
        }

        g_var |= {symbol.name: tuple_variations(glyph, variants)}

        h_metrics |= {symbol.name: (FONT_SIZE, glyph.xMin)}

        # TODO(@ttoino): Ligatures aren't supported yet -- fonttools/fonttools#3423

    font = FontBuilder(FONT_SIZE)
    font.setupGlyphOrder(glyph_order)
    font.setupCharacterMap(char_map)
    font.setupNameTable(
        {
            "familyName": NAME,
            "styleName": STYLE,
            "uniqueFontIdentifier": f"{VERSION};{AUTHOR};{NAME};{STYLE}",
            "fullName": f"{NAME} {STYLE}",
            "psName": f"{NAME}-{STYLE}",
            "version": f"Version {VERSION}",
        }
    )
    font.setupFvar(
        [
            AxisDescriptor(
                tag=AXIS_TAG,
                name=AXIS_NAME,
                minimum=AXIS_MIN,
                maximum=AXIS_MAX,
                default=AXIS_DEFAULT,
                map=[(AXIS_MIN, 0), (AXIS_MAX, 1)],
            )
        ],
        [],
    )
    font.setupGlyf(glyphs)
    font.setupGvar(g_var)
    font.setupHorizontalMetrics(h_metrics)
    font.setupHorizontalHeader(
        ascent=ASCENT,
        descent=DESCENT,
    )
    font.setupOS2(
        sTypoAscent=ASCENT,
        sTypoDescent=DESCENT,
        usWinAscent=ASCENT,
        usWinDescent=abs(DESCENT),
    )
    font.setupPost()

    Path("dist/").mkdir(exist_ok=True)

    font.save(f"dist/{SAFE_NAME}.ttf")

    font.font.flavor = "woff2"
    font.save(f"dist/{SAFE_NAME}.woff2")


if __name__ == "__main__":
    main()
