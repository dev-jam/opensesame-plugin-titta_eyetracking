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
        self.var.sampling_rate_manual = 'no'
        self.var.sampling_rate = ''
        self.var.bimonocular_calibration = 'no'
        self.var.ncalibration_targets = '5'
        self.var.calibration_manual = 'no'
        self.var.calibration_dot = "Thaler (default)"
        self.var.calibration_dot_size = 30
        self.var.calibration_animate = 'yes'
        self.var.calibration_pacing_interval = 1.0
        self.var.calibration_auto_pace = "Autoaccept (default)"
        self.var.calibration_movement_duration = 0.5
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

        self.settings = Titta.get_defaults(self.var.tracker)
        self.settings.FILENAME = self.file_name
        self.settings.DATA_STORAGE_PATH = os.path.dirname(self.var.logfile)
        self.settings.N_CAL_TARGETS = self.var.ncalibration_targets

        if isinstance(self.var.sampling_rate, int):
            self.settings.SAMPLING_RATE = self.var.sampling_rate
            print(f'Using manual sampling rate: {self.settings.SAMPLING_RATE}')
        else:
            print(f'Using default sampling rate: {self.settings.SAMPLING_RATE}')
        if self.var.calibration_manual == 'yes':

            self.settings.graphics.TARGET_SIZE = self.var.calibration_dot_size
            self.settings.graphics.TARGET_SIZE_INNER=self.settings.graphics.TARGET_SIZE / 6  # inner diameter of dot

            if isinstance(self.var.calibration_pacing_interval, float):
                self.PACING_INTERVAL = self.var.calibration_pacing_interval
            else:
                raise OSException('Pacing interval needs to be a decimal/float')

            if isinstance(self.var.calibration_movement_duration, float):
                self.settings.MOVE_TARGET_DURATION = self.var.calibration_movement_duration
            else:
                raise OSException('Movement duration needs to be a decimal/float')

            if self.var.calibration_animate == 'yes':
                self.ANIMATE_CALIBRATION = True
            else:
                self.ANIMATE_CALIBRATION = False

            if self.var.calibration_auto_pace == "Space bar":
                self.AUTO_PACE = 0
            elif self.var.calibration_auto_pace == "Semi autoaccept":
                self.AUTO_PACE = 1
            elif self.var.calibration_auto_pace == "Autoaccept (default)":
                self.AUTO_PACE = 2

            if self.var.calibration_dot == "Thaler (default)":
                self.settings.CAL_TARGET = helpers_tobii.MyDot2(units='pix', outer_diameter=self.settings.graphics.TARGET_SIZE, inner_diameter=self.settings.graphics.TARGET_SIZE_INNER)
            elif self.var.calibration_dot == "Black":
                self.settings.CAL_TARGET = helpers_tobii.MyDot3(units='pix', outer_diameter=self.settings.graphics.TARGET_SIZE, inner_diameter=self.settings.graphics.TARGET_SIZE_INNER)

        if self.var.operator == 'yes':
            # Monitor/geometry operator screen
            MY_MONITOR_OP                  = self.var.screen_name # needs to exists in PsychoPy monitor center
            FULLSCREEN_OP                  = False
            SCREEN_RES_OP                  = [self.var.xres, self.var.yres]
            SCREEN_WIDTH_OP                = 52.7 # cm
            VIEWING_DIST_OP                = 63 #  # distance from eye to center of screen (cm)

            from psychopy import visual, monitors

            mon_op = monitors.Monitor(MY_MONITOR_OP)  # Defined in defaults file
            mon_op.setWidth(SCREEN_WIDTH_OP)          # Width of screen (cm)
            mon_op.setDistance(VIEWING_DIST_OP)       # Distance eye / monitor (cm)
            mon_op.setSizePix(SCREEN_RES_OP)

            self.experiment.window_op = visual.Window(monitor=mon_op,
                                                      fullscr=FULLSCREEN_OP,
                                                      screen=self.var.screen_nr,
                                                      size=SCREEN_RES_OP,
                                                      units='norm',
                                                      waitBlanking=self.experiment.titta_operator_waitblanking)
            self.experiment.cleanup_functions.append(self.experiment.window_op.close)

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

        # set default state
        self.line_edit_sampling_rate.setEnabled(
            self.checkbox_sampling_rate_manual.isChecked())

        # connect to checkbox_sampling_rate_manual
        self.checkbox_sampling_rate_manual.stateChanged.connect(
            self.line_edit_sampling_rate.setEnabled)

        # set default state
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

        # connect to checkbox_calibration_manual
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

        # set default state
        self.line_edit_xres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_yres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_nr.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_name.setEnabled(self.checkbox_operator.isChecked())
        self.checkbox_waitblanking.setEnabled(self.checkbox_operator.isChecked())

        # connect to checkbox_operator
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
