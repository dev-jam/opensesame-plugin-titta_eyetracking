# OpenSesame Plugin: Titta Eye Tracking

*Copyright, 2023, Bob Rosbag, Diederick C. Niehorster & Marcus Nyström*

## About

This plugin implements Titta in OpenSesame for Eye Tracking. 

Titta is a toolbox for using eye trackers from Tobii Pro AB with Python, specifically offering integration with PsychoPy. A Matlab version that integrates with PsychToolbox is also available from https://github.com/dcnieho/Titta. For a similar toolbox for SMI eye trackers, please see www.github.com/marcus-nystrom/SMITE.

Cite as: Niehorster, D.C., Andersson, R. & Nystrom, M. (2020). Titta: A toolbox for creating PsychToolbox and Psychopy experiments with Tobii eye trackers. Behavior Research Methods. doi: 10.3758/s13428-020-01358-8

Please mention: Bob Rosbag as creator of this plugin

For questions, bug reports or to check for updates on Titta, please visit https://github.com/marcus-nystrom/Titta. For the plugin, please visit https://github.com/dev-jam/opensesame-plugin-titta_eyetracking.

To minimize the risk of missing samples, Titta uses TittaPy, a C++ wrapper around the Tobii SDK, to pull samples made available from the eye tracker. TittaPy is installed together with Titta.


## Requirements

- OpenSesame 4.0 or 4.1 with the PsychoPy backend; the items are hidden for other backends.
- Titta 2.2.2 or newer (installed with the plugin).


## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>

This plugin contains works of others.


## Notes

- One recording per experiment is working properly. Per trial recording (multiple starts and stops within an experiment) has not yet been tested.
