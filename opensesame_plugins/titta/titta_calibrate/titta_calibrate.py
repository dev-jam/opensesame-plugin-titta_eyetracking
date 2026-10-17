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


class TittaCalibrate(Item):

    def prepare(self):
        super().prepare()
        self._check_init()

    def run(self):
        self._show_message('Starting calibration')
        self.set_item_onset()
        # Titta's dummy mode has no operator screen
        operator = self.experiment.titta_operator == 'yes' and self.dummy_mode == 'no'
        if self.experiment.titta_bimonocular_calibration == 'yes':
            if operator:
                self._calibrate(self.experiment.window, win_operator=self.experiment.window_op, eye='left',
                                              calibration_number='first')
                self._calibrate(self.experiment.window, win_operator=self.experiment.window_op, eye='right',
                                              calibration_number='second')
            else:
                self._calibrate(self.experiment.window, eye='left',
                                              calibration_number='first')
                self._calibrate(self.experiment.window, eye='right',
                                              calibration_number='second')
        elif self.experiment.titta_bimonocular_calibration == 'no':
            if operator:
                self._calibrate(self.experiment.window, self.experiment.window_op)
            else:
                self._calibrate(self.experiment.window)

    def _calibrate(self, *args, **kwargs):
        # In dummy mode, each calibration starts a thread that simulates gaze;
        # stop the one of an earlier calibration
        if self.dummy_mode == 'yes':
            buffer = getattr(self.experiment.tracker, 'buffer', None)
            if buffer is not None:
                buffer._stop_sample_buffer()
        self.experiment.tracker.calibrate(*args, **kwargs)

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise OSException('You should have one instance of `titta_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class qtTittaCalibrate(TittaCalibrate, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaCalibrate.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
