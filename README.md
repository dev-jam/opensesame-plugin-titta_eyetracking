# OpenSesame Plugin: Titta Eye Tracking

*An OpenSesame plugin for Tobii eye trackers through Titta: calibration, recording, messages and gaze plotting.*

Copyright (C) 2023-2026 Bob Rosbag, Diederick C. Niehorster & Marcus Nyström

## About

This plugin makes Titta available in OpenSesame, for experiments with Tobii eye trackers.

Titta is a toolbox for using eye trackers from Tobii Pro AB with Python, specifically offering integration with PsychoPy. A Matlab version that integrates with PsychToolbox is also available from https://github.com/dcnieho/Titta. For a similar toolbox for SMI eye trackers, please see https://github.com/marcus-nystrom/SMITE.

Cite as: Niehorster, D.C., Andersson, R. & Nystrom, M. (2020). Titta: A toolbox for creating PsychToolbox and Psychopy experiments with Tobii eye trackers. Behavior Research Methods. doi: [10.3758/s13428-020-01358-8](https://doi.org/10.3758/s13428-020-01358-8)

Please mention: Bob Rosbag as creator of this plugin

For questions, bug reports or to check for updates on Titta, please visit https://github.com/marcus-nystrom/Titta. For the plugin, please visit https://github.com/dev-jam/opensesame-plugin-titta_eyetracking.

To minimize the risk of missing samples, Titta uses TittaPy, a C++ wrapper around the Tobii SDK, to pull samples made available from the eye tracker. TittaPy is installed together with Titta.


## Items

- **Titta Init** connects to the eye tracker and sets it up: the eye tracker model, dummy mode, calibration settings and an optional operator screen. Place it at the beginning of the experiment.
- **Titta Calibrate** shows Titta's calibration screen.
- **Titta Start Recording** starts the recording of the chosen data (gaze, time sync, eye images, notifications, external signal, positioning).
- **Titta Send Message** sends a message to the recording, e.g. to mark an event.
- **Titta Plot Gaze** shows the gaze position on the stimulus display and/or the operator display, until a response key is pressed or the timeout has passed.
- **Titta Stop Recording** stops the recording.
- **Titta Save Data** saves the recording as `subject-<nr>.h5` in the folder of the log file (`subject-<nr>_1.h5`, ... when that file exists), and can also export it to tsv files. In dummy mode no data is saved.


## Requirements

- OpenSesame 4.0 or 4.1 with the PsychoPy backend; the items are hidden for other backends.
- Titta 2.2.2 or newer (installed with the plugin).
- PsychoPy, which comes with OpenSesame (it is not installed with the plugin).


## Installation

Install the plugin with pip, in the Python environment of OpenSesame:

    pip install opensesame-plugin-titta-eyetracking


## License

This plugin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version (GPL-3.0-or-later).

The full license text is in the file `COPYING`, and is also available at <https://www.gnu.org/licenses/gpl-3.0.html>.

This plugin contains works of others.


## Notes

- One recording per experiment is working properly. Per trial recording (multiple starts and stops within an experiment) has not yet been tested.
