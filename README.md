# OpenSesame Plugin: Titta Eye Tracking

*Copyright, 2023, Bob Rosbag, Diederick C. Niehorster & Marcus Nyström*

## About

This plugin implements Titta in OpenSesame for Eye Tracking. 

Titta is a toolbox for using eye trackers from Tobii Pro AB with Python, specifically offering integration with PsychoPy. A Matlab version that integrates with PsychToolbox is also available from https://github.com/dcnieho/Titta. For a similar toolbox for SMI eye trackers, please see www.github.com/marcus-nystrom/SMITE.

Cite as: Niehorster, D.C., Andersson, R. & Nystrom, M. (2020). Titta: A toolbox for creating PsychToolbox and Psychopy experiments with Tobii eye trackers. Behavior Research Methods. doi: 10.3758/s13428-020-01358-8

Please mention: Bob Rosbag as creator of this plugin

For questions, bug reports or to check for updates, please visit https://github.com/marcus-nystrom/Titta.

To minimize the risk of missing samples, the current repository uses TittaPy (pip install TittaPy), a C++ wrapper around the Tobii SDK, to pull samples made available from the eye tracker.


## License

The Titta Eye Tracking plugin is distributed under the terms of the Creative Commons Attribution 4.0 International Public License
The full license should be included in the file LICENSE.md


## Known bugs

- In dummy mode, when the experiment is finished, OpenSesame will not return to the GUI. The button with the cross and text: 'Forcibly kill the experiment' has to be used to end the session and get back to the GUI. This only happens when in dummy mode and the cause resides somewhere in the 'calibrate' command.
