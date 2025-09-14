"""Generates the font."""

from pathlib import Path

from fontTools.designspaceLib import AxisDescriptor
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.transform import Identity
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import SVGPath
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables.TupleVariation import TupleVariation

from params import (
    ASCENT,
    AUTHOR,
    AXIS_DEFAULT,
    AXIS_MAX,
    AXIS_MIN,
    AXIS_NAME,
    AXIS_TAG,
    DESCENT,
    FONT_SIZE,
    NAME,
    SAFE_NAME,
    STYLE,
    VERSION,
)
from symbols import SYMBOLS


def glyph_from_path(path: str) -> Glyph:
    """Generate a glyph from an SVG path."""
    svg = SVGPath.fromstring(
        f"""
            <svg xmlns="http://www.w3.org/2000/svg"
                viewBox="0 {-FONT_SIZE} {FONT_SIZE} {FONT_SIZE}"
            >
                <path d="{path}" />
            </svg>
        """,
        # SVG coordinates are mirrored on the Y-axis
        Identity.scale(1, -1),
    )

    ttpen = TTGlyphPen()
    # Fonts don't support cubic bezier curves
    svg.draw(ttpen)

    return ttpen.glyph()


def tuple_variations(base: Glyph, variations: dict[float, str]) -> list[TupleVariation]:
    """Generate tuple variations from the base glyph, coordinates, and paths."""
    # We should only provide the needed deltas,
    # if we provide deltas for all points the font breaks (no idea why).
    # If we provide points only for points that change,
    # neighboring points also get interpolated,
    # so we should also provide deltas for these neighbors.

    variations_list = sorted(variations.items())
    gvar: list[TupleVariation] = []

    for i, (coord, path) in enumerate(variations_list):
        glyph = glyph_from_path(path)

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
    glyph_order = [""]
    char_map: dict[int, str] = {}
    glyphs = {"": Glyph()}
    g_var: dict[str, list[TupleVariation]] = {}
    h_metrics = {"": (0, 0)}

    for symbol in SYMBOLS:
        glyph_order.append(symbol.name)

        char_map |= {
            code: symbol.name for code in symbol.characters if isinstance(code, int)
        }

        glyph = glyph_from_path(symbol.path)
        glyph.recalcBounds(None)
        glyphs[symbol.name] = glyph

        g_var |= {symbol.name: tuple_variations(glyph, symbol.variants)}

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
