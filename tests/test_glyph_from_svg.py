"""Tests for glyph_from_svg()."""

from pathlib import Path

from font_generator import glyph_from_svg

MINIMAL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <path d="M0,0 L100,0 L100,100 L0,100 Z" />
</svg>"""


def test_glyph_from_svg_loads_simple_rectangle(tmp_path: Path) -> None:
    svg_path = tmp_path / "rect.svg"
    svg_path.write_text(MINIMAL_SVG)

    glyph = glyph_from_svg(svg_path)

    assert glyph.numberOfContours == 1
    assert list(glyph.endPtsOfContours) == [3]
    assert len(glyph.coordinates) == 4


def test_glyph_from_svg_applies_y_flip(tmp_path: Path) -> None:
    """SVG coordinates are mirrored on the Y-axis."""
    svg_path = tmp_path / "rect.svg"
    # A rectangle from (0,0) to (100,100) in SVG space
    svg_path.write_text(MINIMAL_SVG)

    glyph = glyph_from_svg(svg_path)

    # After Y-flip, (0,0) becomes (0,0) and (0,100) becomes (0,-100)
    assert glyph.coordinates[0] == (0, 0)
    assert glyph.coordinates[1] == (100, 0)
    assert glyph.coordinates[2] == (100, -100)
    assert glyph.coordinates[3] == (0, -100)
