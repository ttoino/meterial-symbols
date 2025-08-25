"""Generates the font."""

from pathlib import Path

from fontTools.designspaceLib import AxisDescriptor
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.transform import Identity
from fontTools.pens.cu2quPen import Cu2QuPen
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
    ICON_SIZE,
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
                width="{ICON_SIZE}"
                height="{ICON_SIZE}"
                viewBox="0 0 {ICON_SIZE} {ICON_SIZE}"
            >
                <path d="{path}" />
            </svg>
        """,
        # SVG coordinates are mirrored on the Y-axis
        Identity.translate(0, FONT_SIZE).scale(
            FONT_SIZE / ICON_SIZE, -FONT_SIZE / ICON_SIZE
        ),
    )

    ttpen = TTGlyphPen()
    # Fonts don't support cubic bezier curves
    c2qpen = Cu2QuPen(ttpen, 1)
    svg.draw(c2qpen)

    return ttpen.glyph()


def tuple_variation(base: Glyph, variation: tuple[int, str]) -> TupleVariation:
    """Generate a tuple variation from the base glyph, coordinate, and path."""
    glyph = glyph_from_path(variation[1])

    # We should only provide the needed deltas,
    # if we provide deltas for all points the font breaks (no idea why).
    # If we provide points only for points that change,
    # neighboring points also get interpolated,
    # so we should also provide deltas for these neighbors.

    last = 0
    selected: set[int] = set()

    for i in range(glyph.numberOfContours):
        for j in range(last, glyph.endPtsOfContours[i] + 1):
            if glyph.coordinates[j] != base.coordinates[j]:
                selected |= {
                    # Previous point
                    j - 1 if j > last else glyph.endPtsOfContours[i],
                    j,
                    # Next point
                    j + 1 if j < glyph.endPtsOfContours[i] else last,
                }

        last = glyph.endPtsOfContours[i] + 1

    return TupleVariation(
        {AXIS_TAG: (0, (variation[0] - AXIS_MIN) / (AXIS_MAX - AXIS_MIN), 1)},
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

        g_var |= {
            symbol.name: [tuple_variation(glyph, v) for v in symbol.variants.items()]
        }

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
