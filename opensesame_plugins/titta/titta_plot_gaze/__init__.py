"""Titta item to plot gaze"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "response_key",
        "label": "Response key",
        "name": "line_edit_response_key",
        "tooltip": "Expecting a semicolon-separated list of button characters, e.g., a;b;c"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout (ms)",
        "name": "line_edit_timeout",
        "tooltip": "Expecting a value in milliseconds or 'infinite'"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 3.0.0</small>"
    }
]
