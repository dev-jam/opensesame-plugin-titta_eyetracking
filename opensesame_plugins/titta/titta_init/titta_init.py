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

import os

from libopensesame.exceptions import OSException

from ..qt_titta_item import QtTittaItem
from ..titta_item import TittaItem

AUTO_PACE = {
    'Space bar': 0,
    'Semi autoaccept': 1,
    'Autoaccept (default)': 2,
}

# Classes in titta.helpers_tobii
CALIBRATION_DOTS = {
    'Thaler (default)': 'MyDot2',
    'Black': 'MyDot3',
}

# Numbers of calibration targets that Titta accepts
N_CALIBRATION_TARGETS = (0, 1, 3, 5, 9, 13)
# Titta checks this only on a real eye tracker, not in dummy mode
MIN_PACING_INTERVAL = 0.8  # s

# Operator screen
OPERATOR_SCREEN_WIDTH = 52.7  # cm
OPERATOR_VIEWING_DISTANCE = 63  # distance from eye to center of screen (cm)


class TittaInit(TittaItem):

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
        self.var.headbox_manual = 'no'
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
        self._check_single_init()
        self._init_var()
        if self.var.canvas_backend != 'psycho':
            raise OSException('Titta only supports PsychoPy as backend')
        self.settings = self._make_settings()
        if self.operator:
            self._check_operator_screen()

    def run(self):
        from titta import Titta

        self._set_data_file()
        if self.operator:
            self._open_operator_window()

        self._show_message('Initialising Eye Tracker')
        self.set_item_onset()
        with self._titta_errors('initialise the eye tracker'):
            self.experiment.tracker = Titta.Connect(self.settings)
            if self.dummy_mode:
                self._show_message('Dummy mode activated')
                self.experiment.tracker.set_dummy_mode()
                self.experiment.cleanup_functions.append(self._stop_dummy_buffer)
            self.experiment.tracker.init()

    def _init_var(self):
        # Any other value would connect to the eye tracker
        if self.var.dummy_mode not in ('yes', 'no'):
            raise OSException(f"Dummy mode needs to be 'yes' or 'no', not '{self.var.dummy_mode}'")
        self.dummy_mode = self.var.dummy_mode == 'yes'
        self.verbose = self.var.verbose == 'yes'
        self.operator = self.var.operator == 'yes'
        self.waitblanking = self.var.waitblanking == 'yes'
        # Shared state for the other Titta items (and inline scripts)
        self.experiment.titta_recording = None
        self.experiment.titta_dummy_mode = self.var.dummy_mode
        self.experiment.titta_verbose = self.var.verbose
        self.experiment.titta_bimonocular_calibration = self.var.bimonocular_calibration
        self.experiment.titta_operator = self.var.operator
        self.experiment.titta_operator_xres = self.var.xres
        self.experiment.titta_operator_yres = self.var.yres
        self.experiment.titta_operator_screen_nr = self.var.screen_nr
        self.experiment.titta_operator_screen_name = self.var.screen_name
        self.experiment.titta_operator_waitblanking = self.waitblanking

    def _make_settings(self):
        try:
            from titta import Titta, helpers_tobii
        except Exception as e:
            raise OSException(f'Could not import titta: {e}') from e

        # Default settings for the selected tracker
        with self._titta_errors(f'find the settings of {self.var.tracker}'):
            settings = Titta.get_defaults(self.var.tracker)
        settings.N_CAL_TARGETS = self._choice(
            'ncalibration_targets', N_CALIBRATION_TARGETS)
        if self.var.tracker_address:
            settings.TRACKER_ADDRESS = self.var.tracker_address

        if self.var.sampling_rate_manual == 'yes':
            settings.SAMPLING_RATE = self._number(
                'sampling_rate', 'Sampling rate', int)
            self._show_message(f'Using manual sampling rate: {settings.SAMPLING_RATE}')
        else:
            self._show_message(f'Using default sampling rate: {settings.SAMPLING_RATE}')

        if self.var.tracking_mode != 'Default':
            settings.TRACKING_MODE = self.var.tracking_mode
            self._show_message(f'Using tracking mode: {settings.TRACKING_MODE}')

        settings.RECORD_EYE_IMAGES_DURING_CALIBRATION = \
            self.var.record_eye_images_during_calibration == 'yes'

        if self.var.headbox_manual == 'yes':
            center = [self.var.get(f'head_box_center_{axis}') for axis in 'xyz']
            if not all(isinstance(value, (int, float)) for value in center):
                raise OSException('Head box center coordinates must be numbers and have values for three dimensions')
            settings.HEAD_BOX_CENTER = center
            self._show_message(f'Using head box center: {settings.HEAD_BOX_CENTER}')

        if self.var.calibration_manual == 'yes':
            graphics = settings.graphics
            graphics.TARGET_SIZE = self._number(
                'calibration_dot_size', 'Calibration dot size')
            graphics.TARGET_SIZE_INNER = graphics.TARGET_SIZE / 6
            settings.PACING_INTERVAL = self._number(
                'calibration_pacing_interval', 'Pacing interval')
            if settings.PACING_INTERVAL < MIN_PACING_INTERVAL:
                raise OSException(f'Pacing interval needs to be at least {MIN_PACING_INTERVAL} s')
            # 0 is valid: the target jumps to the next position
            settings.MOVE_TARGET_DURATION = self._number(
                'calibration_movement_duration', 'Movement duration', allow_zero=True)
            settings.ANIMATE_CALIBRATION = self.var.calibration_animate == 'yes'
            settings.AUTO_PACE = AUTO_PACE[self._choice(
                'calibration_auto_pace', AUTO_PACE)]
            dot = getattr(helpers_tobii, CALIBRATION_DOTS[self._choice(
                'calibration_dot', CALIBRATION_DOTS)])
            settings.CAL_TARGET = dot(
                units='pix',
                outer_diameter=graphics.TARGET_SIZE,
                inner_diameter=graphics.TARGET_SIZE_INNER
            )
        return settings

    def _set_data_file(self):
        # In the run phase, because an earlier item may set subject_nr
        folder = os.path.dirname(self.var.logfile)
        self.settings.FILENAME = f'subject-{self.var.subject_nr}'
        self.settings.DATA_STORAGE_PATH = folder
        self.experiment.titta_file_name = os.path.normpath(
            os.path.join(folder, self.settings.FILENAME))
        self._show_message(f'Data will be stored in: {self.experiment.titta_file_name}')

    def _open_operator_window(self):
        from psychopy import visual, monitors

        resolution = [self.var.xres, self.var.yres]
        # The monitor needs to exist in the PsychoPy Monitor Center
        monitor = monitors.Monitor(self.var.screen_name)
        monitor.setWidth(OPERATOR_SCREEN_WIDTH)
        monitor.setDistance(OPERATOR_VIEWING_DISTANCE)
        monitor.setSizePix(resolution)
        self.experiment.window_op = visual.Window(
            monitor=monitor,
            fullscr=False,
            screen=self.var.screen_nr,
            size=resolution,
            units='norm',
            waitBlanking=self.waitblanking
        )
        self.experiment.cleanup_functions.append(self.experiment.window_op.close)

    def _check_operator_screen(self):
        self._number('screen_nr', 'Screen number', int, allow_zero=True)
        self._number('xres', 'Resolution X', int)
        self._number('yres', 'Resolution Y', int)

    def _check_single_init(self):
        if hasattr(self.experiment, 'titta_dummy_mode'):
            raise OSException('You should have only one instance of `titta_init` in your experiment')

    def _number(self, var, label, types=(int, float), allow_zero=False):
        value = self.var.get(var)
        if not isinstance(value, types) or value < 0 or (value == 0 and not allow_zero):
            kind = 'integer' if types is int else 'number'
            requirement = f'0 or a positive {kind}' if allow_zero else f'a positive {kind}'
            raise OSException(f'{label} needs to be {requirement}')
        return value

    def _choice(self, var, options):
        value = self.var.get(var)
        if value not in options:
            raise OSException(f'{var} needs to be one of: {", ".join(str(option) for option in options)}')
        return value


class QtTittaInit(TittaInit, QtTittaItem):

    dependent_controls = {
        'checkbox_sampling_rate_manual': ['line_edit_sampling_rate'],
        'checkbox_calibration_manual': [
            'combobox_calibration_dot',
            'line_edit_calibration_dot_size',
            'checkbox_calibration_animate',
            'line_edit_calibration_pacing_interval',
            'combobox_calibration_auto_pace',
            'line_edit_calibration_movement_duration',
        ],
        'checkbox_headbox_manual': [
            'line_edit_head_box_center_x',
            'line_edit_head_box_center_y',
            'line_edit_head_box_center_z',
        ],
        'checkbox_operator': [
            'line_edit_screen_name',
            'line_edit_screen_nr',
            'line_edit_xres',
            'line_edit_yres',
            'checkbox_waitblanking',
        ],
    }

    def __init__(self, name, experiment, script=None):
        TittaInit.__init__(self, name, experiment, script)
        QtTittaItem.__init__(self, __file__)
