"""Titta item to start recording"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "start_gaze",
        "label": "Record gaze",
        "name": "checkbox_start_gaze",
        "tooltip": "Record gaze"
    },  {
        "type": "checkbox",
        "var": "start_time_sync",
        "label": "Record time sync",
        "name": "checkbox_start_time_sync",
        "tooltip": "Record time sync"
    },  {
        "type": "checkbox",
        "var": "start_eye_image",
        "label": "Record eye images",
        "name": "checkbox_start_eye_image",
        "tooltip": "Record eye images"
    },  {
        "type": "checkbox",
        "var": "start_notifications",
        "label": "Record notifications",
        "name": "checkbox_start_notifications",
        "tooltip": "Record notifications"
    },  {
        "type": "checkbox",
        "var": "start_external_signal",
        "label": "Record external signal",
        "name": "checkbox_start_external_signal",
        "tooltip": "Record external signal"
    },  {
        "type": "checkbox",
        "var": "start_positioning",
        "label": "Record positioning",
        "name": "checkbox_start_positioning",
        "tooltip": "Record positioning"
    },  {
        "type": "checkbox",
        "var": "blocking_mode",
        "label": "Block until recording has started",
        "name": "checkbox_blocking_mode",
        "tooltip": "Block until recording has started"
    },  {
        "type": "text",
        "label": "<small><b>Note:</b> A Titta Init item at the beginning of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": f"<small>Titta Eye Tracking version {__version__}</small>"
    }
]


def supports(exp):
    return exp.var.canvas_backend == 'psycho'