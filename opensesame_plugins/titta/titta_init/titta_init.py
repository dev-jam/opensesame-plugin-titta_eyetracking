"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
import os


class TittaInit(Item):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'
        self.var.tracker = 'Tobii Pro Spectrum'
        self.var.tracker_address = ''
        self.var.sampling_rate_manual = 'no'
        self.var.sampling_rate = ''
        self.var.tracking_mode = 'Default'
        self.var.bimonocular_calibration = 'no'
        self.var.ncalibration_targets = '5'
        self.var.calibration_manual = 'no'
        self.var.calibration_dot = "Thaler (default)"
        self.var.calibration_dot_size = 30
        self.var.calibration_animate = 'yes'
        self.var.calibration_pacing_interval = 1.0
        self.var.calibration_auto_pace = "Autoaccept (default)"
        self.var.calibration_movement_duration = 0.5
        self.var.record_eye_images_during_calibration = 'no'
        self.var.head_box_center_x = ''
        self.var.head_box_center_y = ''
        self.var.head_box_center_z = ''
        self.var.operator = 'no'
        self.var.screen_name = 'default'
        self.var.screen_nr = 1
        self.var.xres = '1920'
        self.var.yres = '1080'
        self.var.waitblanking = 'no'

    def prepare(self):
        super().prepare()
        self._init_var()
        self._check_init()

        try:
            from titta import Titta, helpers_tobii
        except Exception:
            raise OSException('Could not import titta')

        if self.var.canvas_backend != 'psycho':
            raise OSException('Titta only supports PsychoPy as backend')

        self.file_name = 'subject-' + str(self.var.subject_nr)
        self.experiment.titta_file_name = os.path.normpath(os.path.join(os.path.dirname(self.var.logfile), self.file_name))
        self._show_message(f'Data will be stored in: {self.file_name}')

        # Get default settings for the selected tracker
        self.settings = Titta.get_defaults(self.var.tracker)

        # Basic settings
        self.settings.FILENAME = self.file_name
        self.settings.DATA_STORAGE_PATH = os.path.dirname(self.var.logfile)

        # Calibration settings
        self.settings.N_CAL_TARGETS = self.var.ncalibration_targets

        # Tracker address
        if self.var.tracker_address:
            self.settings.TRACKER_ADDRESS = self.var.tracker_address

        # Sampling rate
        if isinstance(self.var.sampling_rate, int):
            self.settings.SAMPLING_RATE = self.var.sampling_rate
            print(f'Using manual sampling rate: {self.settings.SAMPLING_RATE}')
        else:
            print(f'Using default sampling rate: {self.settings.SAMPLING_RATE}')

        # Tracking mode
        if self.var.tracking_mode != 'Default':
            self.settings.TRACKING_MODE = self.var.tracking_mode
            self._show_message(f'Using tracking mode: {self.settings.TRACKING_MODE}')

        # Record eye images during calibration
        if self.var.record_eye_images_during_calibration == 'yes':
            self.settings.RECORD_EYE_IMAGES_DURING_CALIBRATION = True
        else:
            self.settings.RECORD_EYE_IMAGES_DURING_CALIBRATION = False

        # Head box center
        if self.var.headbox_manual == 'yes':
            if isinstance(self.var.head_box_center_x, int) and isinstance(self.var.head_box_center_y, int) and isinstance(self.var.head_box_center_z, int):
                self.settings.HEAD_BOX_CENTER = [
                    self.var.head_box_center_x,
                    self.var.head_box_center_y,
                    self.var.head_box_center_z
                ]
                self._show_message(f'Using head box center: {self.settings.HEAD_BOX_CENTER}')
            raise OSException('Head box center coordinates must be integers and have values for three dimensions')

        # Manual calibration settings
        if self.var.calibration_manual == 'yes':
            # Target size
            self.settings.graphics.TARGET_SIZE = self.var.calibration_dot_size
            self.settings.graphics.TARGET_SIZE_INNER = self.settings.graphics.TARGET_SIZE / 6

            # Pacing interval
            if isinstance(self.var.calibration_pacing_interval, float):
                self.settings.PACING_INTERVAL = self.var.calibration_pacing_interval
            else:
                raise OSException('Pacing interval needs to be a decimal/float')

            # Movement duration
            if isinstance(self.var.calibration_movement_duration, float):
                self.settings.MOVE_TARGET_DURATION = self.var.calibration_movement_duration
            else:
                raise OSException('Movement duration needs to be a decimal/float')

            # Animate calibration
            if self.var.calibration_animate == 'yes':
                self.settings.ANIMATE_CALIBRATION = True
            else:
                self.settings.ANIMATE_CALIBRATION = False

            # Auto pace mode
            if self.var.calibration_auto_pace == "Space bar":
                self.settings.AUTO_PACE = 0
            elif self.var.calibration_auto_pace == "Semi autoaccept":
                self.settings.AUTO_PACE = 1
            elif self.var.calibration_auto_pace == "Autoaccept (default)":
                self.settings.AUTO_PACE = 2

            # Calibration dot type
            if self.var.calibration_dot == "Thaler (default)":
                self.settings.CAL_TARGET = helpers_tobii.MyDot2(
                    units='pix',
                    outer_diameter=self.settings.graphics.TARGET_SIZE,
                    inner_diameter=self.settings.graphics.TARGET_SIZE_INNER
                )
            elif self.var.calibration_dot == "Black":
                self.settings.CAL_TARGET = helpers_tobii.MyDot3(
                    units='pix',
                    outer_diameter=self.settings.graphics.TARGET_SIZE,
                    inner_diameter=self.settings.graphics.TARGET_SIZE_INNER
                )

        # Operator screen setup
        if self.var.operator == 'yes':
            # Monitor/geometry operator screen
            MY_MONITOR_OP = self.var.screen_name # needs to exists in PsychoPy monitor center
            FULLSCREEN_OP = False
            SCREEN_RES_OP = [self.var.xres, self.var.yres]
            SCREEN_WIDTH_OP = 52.7  # cm
            VIEWING_DIST_OP = 63  # distance from eye to center of screen (cm)

            from psychopy import visual, monitors

            mon_op = monitors.Monitor(MY_MONITOR_OP)
            mon_op.setWidth(SCREEN_WIDTH_OP)
            mon_op.setDistance(VIEWING_DIST_OP)
            mon_op.setSizePix(SCREEN_RES_OP)

            self.experiment.window_op = visual.Window(
                monitor=mon_op,
                fullscr=FULLSCREEN_OP,
                screen=self.var.screen_nr,
                size=SCREEN_RES_OP,
                units='norm',
                waitBlanking=self.experiment.titta_operator_waitblanking
            )
            self.experiment.cleanup_functions.append(self.experiment.window_op.close)

        # Initialize tracker
        self._show_message('Initialising Eye Tracker')
        self.set_item_onset()
        self.experiment.tracker = Titta.Connect(self.settings)

        if self.var.dummy_mode == 'yes':
            self._show_message('Dummy mode activated')
            self.experiment.tracker.set_dummy_mode()

        self.experiment.tracker.init()

    def _check_init(self):
        if hasattr(self.experiment, 'tracker'):
            raise OSException('You should have only one instance of `titta_init` in your experiment')

    def _init_var(self):
        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.titta_recording = None
        self.experiment.titta_dummy_mode = self.var.dummy_mode
        self.experiment.titta_verbose = self.var.verbose
        self.experiment.titta_bimonocular_calibration = self.var.bimonocular_calibration
        self.experiment.titta_operator = self.var.operator
        self.experiment.titta_operator_xres = self.var.xres
        self.experiment.titta_operator_yres = self.var.yres
        self.experiment.titta_operator_screen_nr = self.var.screen_nr
        self.experiment.titta_operator_screen_name = self.var.screen_name
        if self.var.waitblanking == 'no':
            self.experiment.titta_operator_waitblanking = False
        else:
            self.experiment.titta_operator_waitblanking = True

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaInit(TittaInit, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaInit.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
        self._need_to_set_enabled = True

    def auto_edit_widget(self):
        super().auto_edit_widget()
        if not self._need_to_set_enabled:
            return
        self._need_to_set_enabled = False

        # Sampling rate controls
        self.line_edit_sampling_rate.setEnabled(
            self.checkbox_sampling_rate_manual.isChecked())
        self.checkbox_sampling_rate_manual.stateChanged.connect(
            self.line_edit_sampling_rate.setEnabled)

        # Manual calibration controls
        self.combobox_calibration_dot.setEnabled(
            self.checkbox_calibration_manual.isChecked())
        self.line_edit_calibration_dot_size.setEnabled(
            self.checkbox_calibration_manual.isChecked())
        self.line_edit_calibration_movement_duration.setEnabled(
            self.checkbox_calibration_manual.isChecked())
        self.checkbox_calibration_animate.setEnabled(
            self.checkbox_calibration_manual.isChecked())
        self.combobox_calibration_auto_pace.setEnabled(
            self.checkbox_calibration_manual.isChecked())
        self.line_edit_calibration_pacing_interval.setEnabled(
            self.checkbox_calibration_manual.isChecked())

        self.checkbox_calibration_manual.stateChanged.connect(
            self.combobox_calibration_dot.setEnabled)
        self.checkbox_calibration_manual.stateChanged.connect(
            self.line_edit_calibration_dot_size.setEnabled)
        self.checkbox_calibration_manual.stateChanged.connect(
            self.line_edit_calibration_movement_duration.setEnabled)
        self.checkbox_calibration_manual.stateChanged.connect(
            self.checkbox_calibration_animate.setEnabled)
        self.checkbox_calibration_manual.stateChanged.connect(
            self.combobox_calibration_auto_pace.setEnabled)
        self.checkbox_calibration_manual.stateChanged.connect(
            self.line_edit_calibration_pacing_interval.setEnabled)

        # Head box controls
        self.line_edit_head_box_center_x.setEnabled(self.checkbox_headbox_manual.isChecked())
        self.line_edit_head_box_center_y.setEnabled(self.checkbox_headbox_manual.isChecked())
        self.line_edit_head_box_center_z.setEnabled(self.checkbox_headbox_manual.isChecked())

        self.checkbox_headbox_manual.stateChanged.connect(
            self.line_edit_head_box_center_x.setEnabled)
        self.checkbox_headbox_manual.stateChanged.connect(
            self.line_edit_head_box_center_y.setEnabled)
        self.checkbox_headbox_manual.stateChanged.connect(
            self.line_edit_head_box_center_z.setEnabled)

        # Operator screen controls
        self.line_edit_xres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_yres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_nr.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_name.setEnabled(self.checkbox_operator.isChecked())
        self.checkbox_waitblanking.setEnabled(self.checkbox_operator.isChecked())

        self.checkbox_operator.stateChanged.connect(
            self.line_edit_xres.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_yres.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_screen_nr.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_screen_name.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.checkbox_waitblanking.setEnabled)
