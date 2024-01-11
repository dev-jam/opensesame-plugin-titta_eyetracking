"""Titta item to save data"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "tsv_export",
        "label": "Additionally export data to tsv",
        "name": "checkbox_tsv_export",
        "tooltip": "Additionally export data to tsv"
    },  {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 2.1.2</small>"
    }
]
