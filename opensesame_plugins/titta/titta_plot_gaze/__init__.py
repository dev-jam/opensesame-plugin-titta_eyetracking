"""Titta item to plot gaze"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "stimulus_display",
        "label": "Plot gaze on stimulus display",
        "name": "checkbox_stimulus_display",
        "tooltip": "Plot gaze on display display"
    },  {
        "type": "checkbox",
        "var": "operator_display",
        "label": "Plot gaze on operator display (if selected in the init item)",
        "name": "checkbox_operator_display",
        "tooltip": "Plot gaze on operator display"
    },  {
        "type": "checkbox",
        "var": "simulate_gaze",
        "label": "Simulate gaze in dummy mode",
        "name": "checkbox_simulate_gaze",
        "tooltip": "Simulate gaze in dummy mode"
    },  {
        "type": "checkbox",
        "var": "disable_waitblanking_gaze",
        "label": "Force disabling of waitBlanking for gaze plot on operator screen",
        "name": "checkbox_disable_waitblanking_gaze",
        "tooltip": "Force disabling of waitBlanking for gaze plot on operator screen"
    },  {
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
        "label": "<small>Titta Eye Tracking version 4.0.0</small>"
    }
]
