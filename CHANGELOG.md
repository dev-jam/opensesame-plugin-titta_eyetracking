# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

    
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

[Unreleased]: https://github.com/dev-jam/opensesame-plugin-titta_eyetracking/compare/3.2.0...HEAD
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
