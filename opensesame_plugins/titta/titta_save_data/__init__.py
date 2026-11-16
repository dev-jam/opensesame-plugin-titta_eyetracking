# Copyright (C) 2023-2026 Bob Rosbag <mail@bobrosbag.nl>, Diederick C. Niehorster, Marcus Nyström
# SPDX-License-Identifier: GPL-3.0-or-later

"""Titta Eye Tracking - saves the recorded data"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "tsv_export",
        "label": "Additionally export data to tsv files",
        "name": "checkbox_tsv_export",
        "tooltip": "Additionally export data to tsv files"
    }, {
        "type": "checkbox",
        "var": "png_export",
        "label": "Additionally export eye images to png files",
        "name": "checkbox_png_export",
        "tooltip": "Additionally export eye images to png files"
    }, {
        "type": "text",
        "label": "<small>A failed export is a warning in the log; the experiment continues</small>"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> A Titta Init item at the beginning of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": f"<small>Titta Eye Tracking version {__version__}</small>"
    }
]


def supports(exp):
    return exp.var.canvas_backend == 'psycho'