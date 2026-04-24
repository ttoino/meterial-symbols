"""Integration test for the full font build pipeline."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest
from fontTools.ttLib import TTFont

from font_generator import main

if TYPE_CHECKING:
    from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p
    from fontTools.ttLib.tables._f_v_a_r import table__f_v_a_r
    from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
    from fontTools.ttLib.tables._g_v_a_r import table__g_v_a_r
    from fontTools.ttLib.tables.TupleVariation import TupleVariation

MINIMAL_SYMBOLS_JSON = [
    {
        "name": "test_square",
        "codepoints": ["0xE000"],
        "ligatures": ["test_square"],
    }
]

# Simple square SVG with viewBox matching the project's coordinate system
BASE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
    <path d="M100,-100 L860,-100 L860,-860 L100,-860 Z" />
</svg>"""

# Same shape but with one point moved to create a variation
VARIANT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
    <path d="M100,-100 L900,-100 L860,-860 L100,-860 Z" />
</svg>"""


def test_main_builds_valid_font(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end build produces a well-formed variable font."""
    monkeypatch.chdir(tmp_path)

    # Create minimal project structure
    symbols_dir = tmp_path / "symbols" / "test_square"
    symbols_dir.mkdir(parents=True)
    (tmp_path / "symbols.json").write_text(json.dumps(MINIMAL_SYMBOLS_JSON))
    (symbols_dir / "_.svg").write_text(BASE_SVG)
    (symbols_dir / "1.svg").write_text(VARIANT_SVG)

    main()

    ttf_path = tmp_path / "dist" / "MeterialSymbols.ttf"
    woff2_path = tmp_path / "dist" / "MeterialSymbols.woff2"

    assert ttf_path.exists()
    assert woff2_path.exists()
    assert ttf_path.stat().st_size > 0
    assert woff2_path.stat().st_size > 0

    # Validate TTF tables and metadata
    font = TTFont(str(ttf_path))

    assert "fvar" in font
    assert "gvar" in font
    assert "glyf" in font
    assert "cmap" in font

    fvar = cast("table__f_v_a_r", font["fvar"])
    assert len(fvar.axes) == 1
    axis = fvar.axes[0]
    assert axis.axisTag == "PGRS"
    assert axis.minValue == 0
    assert axis.maxValue == 100
    assert axis.defaultValue == 0

    cmap = cast("table__c_m_a_p", font["cmap"])
    best_cmap = cmap.getBestCmap()
    assert best_cmap is not None
    assert 0xE000 in best_cmap
    assert best_cmap[0xE000] == "test_square"

    glyf = cast("table__g_l_y_f", font["glyf"])
    assert "test_square" in glyf.glyphs

    gvar = cast("table__g_v_a_r", font["gvar"])
    assert "test_square" in gvar.variations
    # We supplied one variant (1.0) so there should be one tuple variation
    symbol_variations = cast("list[TupleVariation]", gvar.variations["test_square"])
    assert len(symbol_variations) == 1
