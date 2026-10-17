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

from libopensesame.exceptions import OSException

from ..titta_item import TittaItem


class TittaStartRecording(TittaItem):

    def reset(self):
        self.var.start_gaze = 'yes'
        self.var.start_time_sync = 'yes'
        self.var.start_eye_image = 'no'
        self.var.start_notifications = 'yes'
        self.var.start_external_signal = 'yes'
        self.var.start_positioning = 'yes'
        self.var.blocking_mode = 'yes'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()
        self.experiment.titta_start_recording = True

    def run(self):
        self._check_stop()
        self.set_item_onset()
        self.experiment.tracker.start_recording(
            gaze=self.start_gaze,
            time_sync=self.start_time_sync,
            eye_image=self.start_eye_image,
            notifications=self.start_notifications,
            external_signal=self.start_external_signal,
            positioning=self.start_positioning,
            block_until_data_available=self.blocking_mode
        )
        self.experiment.titta_recording = True

    def _init_var(self):
        self.blocking_mode = self.var.blocking_mode == 'yes'
        self.start_gaze = self.var.start_gaze == 'yes'
        self.start_time_sync = self.var.start_time_sync == 'yes'
        self.start_eye_image = self.var.start_eye_image == 'yes'
        self.start_notifications = self.var.start_notifications == 'yes'
        self.start_external_signal = self.var.start_external_signal == 'yes'
        self.start_positioning = self.var.start_positioning == 'yes'

    def _check_stop(self):
        if not hasattr(self.experiment, 'titta_stop_recording'):
            raise OSException('`Titta Stop Recording` item is missing')
        if self.experiment.titta_recording:
            raise OSException('Titta still recording, you first have to stop recording before starting')
