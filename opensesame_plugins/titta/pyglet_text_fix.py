"""
This file is part of opensesame-plugin-titta_eyetracking.

Copyright (C) 2023-2026 Bob Rosbag <mail@bobrosbag.nl>, Diederick C. Niehorster, Marcus Nyström

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later

Work around a pyglet 1.x bug that breaks all PsychoPy text on Windows
with Python 3.12 and later (Titta's calibration screens use text).

pyglet 1.x declares the bitmap argument of GDI+'s
GdipCreateBitmapFromScan0 as POINTER(ctypes.wintypes.BYTE), but its
font code passes an array of c_byte. Up to Python 3.11 wintypes.BYTE
was c_byte; since Python 3.12 it is c_ubyte, and ctypes refuses the
call: "ctypes.ArgumentError: argument 5: TypeError: expected
LP_c_ubyte instance instead of c_byte_Array_...". PsychoPy pins
pyglet 1.4.11 on Windows; pyglet 2.x has the fix.
"""

__author__ = "Bob Rosbag"
__license__ = "GPL-3.0-or-later"

import sys

# The argument of GdipCreateBitmapFromScan0 that gets the bitmap data
BITMAP_ARGUMENT = 4


def fix_pyglet_text():
    """Let pyglet's GdipCreateBitmapFromScan0 accept its own c_byte
    array, by declaring the bitmap argument as c_void_p (which accepts
    any array or pointer). Only on Windows, Python 3.12 or later and
    pyglet 1.x, and only while the argument is still declared as
    POINTER(wintypes.BYTE). The function object is shared, so pyglet's
    font code uses the new declaration.

    Returns
    -------
    bool
        True when the declaration was changed.
    """
    if sys.platform != 'win32' or sys.version_info < (3, 12):
        return False
    import ctypes.wintypes
    import pyglet
    if not pyglet.version.startswith('1.'):
        return False
    from pyglet.image.codecs.gdiplus import gdiplus
    function = gdiplus.GdipCreateBitmapFromScan0
    argtypes = list(function.argtypes)
    if argtypes[BITMAP_ARGUMENT] is not ctypes.POINTER(ctypes.wintypes.BYTE):
        return False
    argtypes[BITMAP_ARGUMENT] = ctypes.c_void_p
    function.argtypes = argtypes
    return True
