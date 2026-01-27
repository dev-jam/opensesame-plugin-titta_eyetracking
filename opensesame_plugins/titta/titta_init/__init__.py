"""Titta initialisation item"""

# The category determines the group for the plugin in the item toolbar
category = "Titta Eye Tracking"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "dummy_mode",
        "label": "Dummy mode",
        "name": "checkbox_dummy_mode",
        "tooltip": "Run in dummy mode"
    },  {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose mode",
        "name": "checkbox_verbose_mode",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "combobox",
        "var": "tracker",
        "label": "Select Eye Tracker",
        "options": [
            "Tobii Pro Spectrum",
            "Tobii Pro Fusion",
            "Tobii Pro X3-120 EPU",
            "Tobii Pro X3-120",
            "Tobii Pro Nano",
            "Tobii Pro Spark",
            "Tobii TX300",
            "Tobii T60 XL",
            "Tobii T60",
            "Tobii T120",
            "Tobii X60",
            "Tobii X120",
            "X2-60_Compact",
            "X2-30_Compact",
            "Tobii X120"
        ],
        "name": "combobox_tracker",
        "tooltip": "Select an Eye Tracker"
    },  {
        "type": "checkbox",
        "var": "sampling_rate_manual",
        "label": "Manual Sampling Rate",
        "name": "checkbox_sampling_rate_manual",
        "tooltip": "Enable manual sampling rate"
    }, {
        "type": "line_edit",
        "var": "sampling_rate",
        "label": "Sampling Rate (Hz)",
        "name": "line_edit_sampling_rate",
        "tooltip": "Integer value"
    },  {
        "type": "checkbox",
        "var": "bimonocular_calibration",
        "label": "Bimonocular Calibration",
        "name": "checkbox_bimonocular_calibration",
        "tooltip": "Bimonocular Calibration"
    },  {
        "type": "combobox",
        "var": "ncalibration_targets",
        "label": "Number of calibration targets",
        "options": [
            "0",
            "1",
            "5",
            "9",
            "13"
        ],
        "name": "combobox_ncal",
        "tooltip": "Number of calibration targets"
    },  {
        "type": "checkbox",
        "var": "calibration_manual",
        "label": "Manual calibration settings",
        "name": "checkbox_calibration_manual",
        "tooltip": "Enable manual calibration settings"
    },  {
        "type": "combobox",
        "var": "calibration_dot",
        "label": "Calibration dot type",
        "options": [
            "Thaler (default)",
            "Black"
        ],
        "name": "combobox_calibration_dot",
        "tooltip": "Select a calibration dot type"
    }, {
        "type": "line_edit",
        "var": "calibration_dot_size",
        "label": "Calibration dot size",
        "name": "line_edit_calibration_dot_size",
        "tooltip": "Integer value"
    },  {
        "type": "checkbox",
        "var": "calibration_animate",
        "label": "Animate_calibration",
        "name": "checkbox_calibration_animate",
        "tooltip": "Static or animated calibration dots"
    }, {
        "type": "line_edit",
        "var": "calibration_pacing_interval",
        "label": "Calibration pacing interval",
        "name": "line_edit_calibration_pacing_interval",
        "tooltip": "How long to present the target at calibration/validation location until samples are collected (Float value)"
    },  {
        "type": "combobox",
        "var": "calibration_auto_pace",
        "label": "Calibration auto pace",
        "options": [
            "Space bar",
            "Semi autoaccept",
            "Autoaccept (default)"
        ],
        "name": "combobox_calibration_auto_pace",
        "tooltip": "accept all points with space bar, semi autoaccept (accept only first point with space bar, default), or autoaccept)"
    }, {
        "type": "line_edit",
        "var": "calibration_movement_duration",
        "label": "Movement duration (lower is faster)",
        "name": "line_edit_calibration_movement_duration",
        "tooltip": "Duration for calibration/validation target to move from one position to the next (Float value)"
    },  {
        "type": "checkbox",
        "var": "operator",
        "label": "Operator Screen",
        "name": "checkbox_operator",
        "tooltip": "Enable operator screen"
    },  {
        "type": "line_edit",
        "var": "screen_name",
        "label": "Screen name",
        "name": "line_edit_screen_name",
        "tooltip": "String value"
    },  {
        "type": "line_edit",
        "var": "screen_nr",
        "label": "Screen number",
        "name": "line_edit_screen_nr",
        "tooltip": "Integer value"
    },  {
        "type": "line_edit",
        "var": "xres",
        "label": "Resolution X (pxs)",
        "name": "line_edit_xres",
        "tooltip": "Value in pxs"
    },  {
        "type": "line_edit",
        "var": "yres",
        "label": "Resolution Y (pxs)",
        "name": "line_edit_yres",
        "tooltip": "Value in pxs"
    },  {
        "type": "checkbox",
        "var": "waitblanking",
        "label": "Enable waitBlanking on operator screen",
        "name": "checkbox_waitblanking",
        "tooltip": "Enable waitBlanking on operator screen"
    },  {
        "type": "text",
        "label": "\n\nTitta is a toolbox for using eye trackers from Tobii Pro AB with Python, specifically offering integration with PsychoPy.\n\n\
Cite as:\n\nNiehorster, D.C., Andersson, R. & Nystrom, M. (2020). Titta: A toolbox for creating PsychToolbox and Psychopy experiments with Tobii eye trackers. Behavior Research Methods. doi: 10.3758/s13428-020-01358-8\n\n\
Please mention: Bob Rosbag as creator of this plugin\n\n\
For questions, bug reports or to check for updates on Titta, please visit https://github.com/marcus-nystrom/Titta.\n\n\
To minimize the risk of missing samples, the current repository uses TittaPy (pip install TittaPy), a C++ wrapper around the Tobii SDK, to pull samples made available from the eye tracker."
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Titta Init item at the begin of the experiment is needed for initialization of the Eye Tracker</small>"
    }, {
        "type": "text",
        "label": "<small>Titta Eye Tracking version 6.0.0</small>"
    }
]


def supports(exp):
    return exp.var.canvas_backend == 'psycho'
