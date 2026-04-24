"""Unit tests for tuple_variations()."""

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import Glyph

from font_generator import AXIS_TAG, tuple_variations


def _square_glyph() -> Glyph:
    """Return a simple square glyph with 4 points."""
    pen = TTGlyphPen()
    pen.moveTo((0, 0))
    pen.lineTo((100, 0))
    pen.lineTo((100, 100))
    pen.lineTo((0, 100))
    pen.closePath()
    return pen.glyph()


def test_empty_variations_returns_empty() -> None:
    base = _square_glyph()
    result = tuple_variations(base, {})
    assert result == []


def test_unchanged_points_get_none_deltas() -> None:
    base = _square_glyph()
    variant = _square_glyph()  # identical to base
    result = tuple_variations(base, {0.5: variant})

    assert len(result) == 1
    tv = result[0]
    assert tv.axes == {AXIS_TAG: (0, 0.5, 1)}
    assert all(d is None for d in tv.coordinates)


def test_changed_point_and_neighbors_get_deltas() -> None:
    base = _square_glyph()
    variant = _square_glyph()
    # Move point 1 from (100, 0) to (150, 0)
    variant.coordinates[1] = (150, 0)

    result = tuple_variations(base, {0.5: variant})

    assert len(result) == 1
    tv = result[0]

    # Point 1 changed
    assert tv.coordinates[1] == (50, 0)
    # Neighbors of point 1 in a single contour: 0 and 2
    assert tv.coordinates[0] == (0, 0)
    assert tv.coordinates[2] == (0, 0)
    # Point 3 is unchanged and not a neighbor
    assert tv.coordinates[3] is None


def test_multiple_variations_peak_coords() -> None:
    base = _square_glyph()

    v1 = _square_glyph()
    v1.coordinates[1] = (150, 0)

    v2 = _square_glyph()
    v2.coordinates[1] = (200, 0)

    result = tuple_variations(base, {0.25: v1, 0.75: v2})

    assert len(result) == 2

    # First variation: prev=0, peak=0.25, next=0.75
    assert result[0].axes == {AXIS_TAG: (0, 0.25, 0.75)}
    # Second variation: prev=0.25, peak=0.75, next=1
    assert result[1].axes == {AXIS_TAG: (0.25, 0.75, 1)}


def test_wrapped_neighbor_selection() -> None:
    """When the first or last point in a contour changes, neighbors wrap correctly."""
    base = _square_glyph()
    variant = _square_glyph()
    # Move point 0 from (0, 0) to (0, -10)
    variant.coordinates[0] = (0, -10)

    result = tuple_variations(base, {0.5: variant})

    tv = result[0]
    # Point 0 changed
    assert tv.coordinates[0] == (0, -10)
    # Neighbors of point 0 wrap: 3 (previous) and 1 (next)
    assert tv.coordinates[3] == (0, 0)
    assert tv.coordinates[1] == (0, 0)
    # Point 2 is untouched
    assert tv.coordinates[2] is None
