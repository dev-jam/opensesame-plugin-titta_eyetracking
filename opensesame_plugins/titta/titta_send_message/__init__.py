"""Titta item to send a message to the Eye Tracker"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "message",
        "label": "Send message to the Eye Tracker",
        "name": "line_edit_message",
        "tooltip": "Message"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 1.1.0</small>"
    }
]
