"""Titta item to start recording"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "start_gaze",
        "label": "Record gaze",
        "name": "checkbox_start_gaze",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "start_time_sync",
        "label": "Record time sync",
        "name": "checkbox_start_time_sync",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "start_eye_image",
        "label": "Record eye images",
        "name": "checkbox_start_eye_image",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "start_notifications",
        "label": "Record notifications",
        "name": "checkbox_start_notifications",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "start_external_signal",
        "label": "Record external signal",
        "name": "checkbox_start_external_signal",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "start_positioning",
        "label": "Record positioning",
        "name": "checkbox_start_positioning",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "blocking_mode",
        "label": "Block until recording has started",
        "name": "checkbox_blocking_mode",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 4.0.0</small>"
    }
]
