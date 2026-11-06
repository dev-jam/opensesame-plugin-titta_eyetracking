"""
This file is part of opensesame-plugin-titta_eyetracking.

Copyright (C) 2023-2026 Bob Rosbag <mail@bobrosbag.nl>, Diederick C. Niehorster, Marcus Nyström

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

__author__ = "Bob Rosbag"
__license__ = "GPL-3.0-or-later"

from ..titta_item import STREAMS, TittaItem


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
        self._check_not_recording('starting')
        self.set_item_onset()
        with self._titta_errors('start recording'):
            self.experiment.tracker.start_recording(
                **self.streams,
                block_until_data_available=self.blocking_mode
            )
        self.experiment.titta_recording = True

    def _init_var(self):
        self.blocking_mode = self.var.blocking_mode == 'yes'
        self.streams = {stream: self.var.get(f'start_{stream}') == 'yes'
                        for stream in STREAMS}
