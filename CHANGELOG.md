# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

- fixed: require titta 2.2.2 or newer: titta 2.1.0 doesn't work with TittaPy 2 (No module named 'TittaPy'), and with titta 2.2.0 and 2.2.1 *Block until recording has started* (on by default) fails on a real eye tracker
- fixed: errors reported by Titta (e.g. eye tracker not found, unsupported sampling rate or tracking mode, monocular calibration on a tracker that can't do it) were shown as "An unexpected error occurred"; they now show Titta's message
- fixed: a calibration pacing interval below 0.8 s and an invalid number of calibration targets were accepted in dummy mode (Titta only checks them on a real eye tracker); they are now errors in the prepare phase, also in dummy mode. 3 calibration targets (accepted by Titta) is allowed
- fixed: invalid operator screen settings (screen number, resolution) gave an unclear error, or hung the experiment (a resolution of 0); they are now checked in the prepare phase
- head box center coordinates may have decimals (were whole numbers only)
- fixed: plot gaze kept a CPU core busy while waiting for a key when no gaze is drawn (no display selected, or dummy mode without *Simulate gaze*)
- GUI: labels say that response keys are separated by ;, the timeout can be infinite and the pacing interval must be at least 0.8 s; typo in the note of all items
- readme: requirements, where to report plugin bugs, typo

## [7.0.1] - 2026-10-18

- fix dummy mode: the experiment did not end after a calibration
- fix manual head box center: always gave an error
- fix manual sampling rate: was also used with *Manual Sampling Rate* unchecked, and an invalid value was ignored
- fix calibration pacing interval and movement duration: whole numbers gave an error, also the default pacing interval 1.0
- check the calibration dot size
- fix bimonocular calibration with operator screen in dummy mode
- fix tsv export: used an older data file when the data file of the subject already existed
- fix plot gaze: error with an empty response key, and spaces around response keys were not removed
- fix plot gaze: the list of response keys grew on every keyboard check
- fix send message: a numeric message gave an error in dummy mode; messages are now always sent as text
- fix init item: controls were enabled while their checkbox was unchecked
- remove duplicate Tobii X120 from the eye tracker list
- code cleanup: shared base class for the items, booleans for checkbox settings, no py3compat, GUI classes only where needed
- connect to the eye tracker and open the operator screen in the run phase; the data file uses the subject number at that moment
- plot gaze: *Force disabling of waitBlanking* is only enabled when *Plot gaze on operator display* is checked
- pacing interval and dot size need to be positive, movement duration 0 or more (0: the target jumps); an unknown calibration dot or auto pace value gives an error
- start/stop recording: a setting other than yes or no counts as no (was an error)
- sampling rate message only in verbose mode; tsv export warnings always in the log
- show the reason when titta can't be imported
- fix tooltips
- the version label of the items is read from the installed package
- declare psychopy as dependency (imported directly); drop tittapy (titta installs it)

## [6.1.1] - 2026-09-01

- fixed missing variable

## [6.1.0] - 2026-01-30

- more custom calibration options

## [6.0.0] - 2026-01-27

- Add manual sampling rate
- small code cleanup

## [5.2.0] - 2026-01-22

- Add custom calibration options
- fix Inconsistent UI state initialization in QtAutoPlugin (Qt6) #829

## [5.1.0] - 2026-01-19

- fix Error export data to tsv external signal #2

## [5.0.0] - 2025-12-11

- change incompatible CC BY 4.0 license to GPLv3

## [4.2.0] - 2025-09-05

- convert string handling to f-strings

## [4.1.0] - 2025-07-17

- license cleanup
- disable items when PsychoPy is not selected as backend

## [4.0.1] - 2025-01-28

- small bugfix in stop_recording
    
## [4.0.0] - 2024-11-21

- implemented blocking in start_recording
- fine-grained options in start/stop recording
    
## [3.4.0] - 2024-10-05

- new icons
- checkboxes are not disabled on initialisation so revert
    
## [3.3.0] - 2024-10-01

- getMovieFrame() was replaced with \_getFrame()
    
## [3.2.0] - 2024-09-30

- add simulate gaze
    
## [3.1.0] - 2024-09-30

- separate gaze plot option for experiment and operator screen
- global and local option to disable wait for blanking for operator screen
- internal debug timers for screen drawing
- internal debug option for simulating gaze plotting
    
## [3.0.1] - 2024-09-27

- comment test code
- reordering of code
- dummy mode only inhibits gaze plotting
    
## [3.0.0] - 2024-09-26

- added gaze plot item
- code cleanup
    
## [2.5.0] - 2024-09-23

- added operator / dual screen back
    
## [2.4.0] - 2024-09-02

- reverted dual screen / operator screen option, needs more testing
    
## [2.3.0] - 2024-09-01

Warning:

The structure of the interface has been updated; 'stop recording' and 'save data' are now two distinct items.

﻿Please note that experiments created using version 1.x of the plugin will not save the eye tracking data if run with version 2.x, so it is recommended to ensure compatibility before proceeding.

These modifications were necessary to resolve issues with per-trial recording.

- added dual screen / operator screen option
- save eye images
    
## [2.2.0] - 2024-05-24

Warning:

The structure of the interface has been updated; 'stop recording' and 'save data' are now two distinct items.

﻿Please note that experiments created using version 1.x of the plugin will not save the eye tracking data if run with version 2.x, so it is recommended to ensure compatibility before proceeding.

These modifications were necessary to resolve issues with per-trial recording.

- save external signal and calibration history as tsv data
    
## [2.1.2] - 2024-01-11

Warning:

The structure of the interface has been updated; 'stop recording' and 'save data' are now two distinct items.

﻿Please note that experiments created using version 1.x of the plugin will not save the eye tracking data if run with version 2.x, so it is recommended to ensure compatibility before proceeding.

These modifications were necessary to resolve issues with per-trial recording.

- fixed icon 'save data' item
- added data export as tsv files with checkbox
    
## [2.1.1] - 2024-01-11

Warning:

The structure of the interface has been updated; 'stop recording' and 'save data' are now two distinct items.

﻿Please note that experiments created using version 1.x of the plugin will not save the eye tracking data if run with version 2.x, so it is recommended to ensure compatibility before proceeding.

These modifications were necessary to resolve issues with per-trial recording.

- fixed icon 'save data' item
- added data export as tsv files
    
## [2.0.0] - 2024-01-09

Warning:

The structure of the interface has been updated; 'stop recording' and 'save data' are now two distinct items.

﻿Please note that experiments created using version 1.x of the plugin will not save the eye tracking data if run with version 2.x, so it is recommended to ensure compatibility before proceeding.

These modifications were necessary to resolve issues with per-trial recording.
    
## [1.1.0] - 2023-12-04

- fixed item dependency checks when running an experiment
    
## [1.0.2] - 2023-08-30

- fixed dependencies
- save tobii data to log file folder
    
## [1.0.0] - 2023-08-15

- new style api OpenSesame 4.0

    
## [0.5.0] - 2023-08-13

Final release for OpenSesame 3 API

- small bugfixes
    
## [v0.4.0] - 2023-07-06

- Corrected license
-  Added more info on psychopy monitors
- added item checks
    
## [v0.3.0] - 2023-07-05

Lots of polishing

## v0.2.1 - 2023-07-04

Initial release of OpenSesame Eye Tracking plugin with Titta.

[Unreleased]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/7.0.1...HEAD
[7.0.1]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/6.1.1...7.0.1
[6.1.1]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/6.1.0...6.1.1
[6.1.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/6.0.0...6.1.0
[6.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/5.2.0...6.0.0
[5.2.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/5.1.0...5.2.0
[5.1.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/5.0.0...5.1.0
[5.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/4.2.0...5.0.0
[4.2.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/4.1.0...4.2.0
[4.1.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/4.0.1...4.1.0
[4.0.1]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/4.0.0...4.0.1
[4.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.4.0...4.0.0
[3.4.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.3.0...3.4.0
[3.3.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.2.0...3.3.0
[3.2.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.1.0...3.2.0
[3.1.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.5.0...3.0.0
[2.5.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.4.0...2.5.0
[2.4.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.2.0...2.3.0
[2.2.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.1.2...2.2.0
[2.1.2]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.1.1...2.1.2
[2.1.1]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/2.0.0...2.1.1
[2.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/1.1.0...2.0.0
[1.1.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/1.0.2...1.1.0
[1.0.2]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/1.0.0...1.0.2
[1.0.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/0.5.0...1.0.0
[0.5.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/v0.4.0...0.5.0
[v0.4.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/v0.2.1...v0.3.0
