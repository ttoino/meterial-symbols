"""Defines some constants used in the creation of the font."""

import re

NAME = "Meterial Symbols"
"""The font name"""
SAFE_NAME = re.sub(r"\W", "", NAME)
STYLE = "Regular"
"""The font style"""
VERSION = "1.0.0"
"""The font version"""
AUTHOR = "Toino"
"""The font author"""

ICON_SIZE = 24
"""The size of the SVG canvas used to draw the icons"""
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
