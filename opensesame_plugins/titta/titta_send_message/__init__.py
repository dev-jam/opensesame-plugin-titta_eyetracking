"""Titta item to send a message to the Eye Tracker"""

from .. import __version__

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
        "label": "<small><b>Note:</b> A Titta Init item at the beginning of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": f"<small>Titta Eye Tracking version {__version__}</small>"
    }
]


def supports(exp):
    return exp.var.canvas_backend == 'psycho'