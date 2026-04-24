"""Tests that all SVG variants for each symbol are structurally compatible."""

from pathlib import Path

import pytest

from font_generator import glyph_from_svg

SYMBOLS_DIR = Path("symbols")


def _get_symbol_names() -> list[str]:
    return sorted(p.name for p in SYMBOLS_DIR.iterdir() if p.is_dir())


@pytest.mark.parametrize("symbol_name", _get_symbol_names())
def test_symbol_variants_have_same_structure(symbol_name: str) -> None:
    """Every SVG for a symbol must have the same contour/point structure."""
    base_path = SYMBOLS_DIR / symbol_name
    svgs = sorted(base_path.glob("*.svg"))
    assert svgs, f"No SVGs found for symbol {symbol_name}"

    glyphs = [glyph_from_svg(svg) for svg in svgs]
    base_glyph = glyphs[0]

    for svg, glyph in zip(svgs[1:], glyphs[1:], strict=True):
        assert glyph.numberOfContours == base_glyph.numberOfContours, (
            f"{symbol_name}: {svg.name} has {glyph.numberOfContours} contours, "
            f"expected {base_glyph.numberOfContours} (from {svgs[0].name})"
        )
        assert list(glyph.endPtsOfContours) == list(base_glyph.endPtsOfContours), (
            f"{symbol_name}: {svg.name} has endPtsOfContours "
            f"{list(glyph.endPtsOfContours)}, expected "
            f"{list(base_glyph.endPtsOfContours)} (from {svgs[0].name})"
        )
