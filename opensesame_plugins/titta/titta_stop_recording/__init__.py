"""Titta item to stop recording"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "stop_gaze",
        "label": "Stop recording gaze",
        "name": "checkbox_stop_gaze",
        "tooltip": "Stop recording gaze"
    },  {
        "type": "checkbox",
        "var": "stop_time_sync",
        "label": "Stop recording time sync",
        "name": "checkbox_stop_time_sync",
        "tooltip": "Stop recording time sync"
    },  {
        "type": "checkbox",
        "var": "stop_eye_image",
        "label": "Stop recording eye images",
        "name": "checkbox_stop_eye_image",
        "tooltip": "Stop recording eye images"
    },  {
        "type": "checkbox",
        "var": "stop_notifications",
        "label": "Stop recording notifications",
        "name": "checkbox_stop_notifications",
        "tooltip": "Stop recording notifications"
    },  {
        "type": "checkbox",
        "var": "stop_external_signal",
        "label": "Stop recording external signal",
        "name": "checkbox_stop_external_signal",
        "tooltip": "Stop recording external signal"
    },  {
        "type": "checkbox",
        "var": "stop_positioning",
        "label": "Stop recording positioning",
        "name": "checkbox_stop_positioning",
        "tooltip": "Stop recording positioning"
    },  {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 6.1.1</small>"
    }
]


def supports(exp):
    return exp.var.canvas_backend == 'psycho'