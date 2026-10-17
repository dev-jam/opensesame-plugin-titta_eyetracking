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

from ..titta_item import TittaItem


class TittaCalibrate(TittaItem):

    def prepare(self):
        super().prepare()
        self._check_init()
        self.bimonocular_calibration = self.experiment.titta_bimonocular_calibration == 'yes'
        # Titta's dummy mode has no operator screen
        self.operator = self.experiment.titta_operator == 'yes' and not self.dummy_mode

    def run(self):
        self._show_message('Starting calibration')
        self.set_item_onset()
        kwargs = {'win_operator': self.experiment.window_op} if self.operator else {}
        if self.bimonocular_calibration:
            self._calibrate(eye='left', calibration_number='first', **kwargs)
            self._calibrate(eye='right', calibration_number='second', **kwargs)
        else:
            self._calibrate(**kwargs)

    def _calibrate(self, **kwargs):
        if self.dummy_mode:
            # Each calibration starts a new thread that simulates gaze
            self._stop_dummy_buffer()
        self.experiment.tracker.calibrate(self.experiment.window, **kwargs)
