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

from ..titta_item import STREAMS, TittaItem


class TittaStopRecording(TittaItem):

    def reset(self):
        self.var.stop_gaze = 'yes'
        self.var.stop_time_sync = 'yes'
        self.var.stop_eye_image = 'no'
        self.var.stop_notifications = 'yes'
        self.var.stop_external_signal = 'yes'
        self.var.stop_positioning = 'yes'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()
        self.experiment.titta_stop_recording = True

    def run(self):
        self._check_start()
        self.set_item_onset()
        with self._titta_errors('stop recording'):
            self.experiment.tracker.stop_recording(**self.streams)
        self.experiment.titta_recording = False

    def _init_var(self):
        self.streams = {stream: self.var.get(f'stop_{stream}') == 'yes'
                        for stream in STREAMS}

    def _check_start(self):
        if not hasattr(self.experiment, 'titta_start_recording'):
            raise OSException('`Titta Start Recording` item is missing')
        if not self.experiment.titta_recording:
            raise OSException('Titta not recording, you first have to start recording before stopping')
