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

from ..titta_item import TittaItem


class TittaSendMessage(TittaItem):

    def reset(self):
        self.var.message = 'onset_stimulusname'

    def prepare(self):
        super().prepare()
        self._check_init()

    def run(self):
        self.set_item_onset()
        with self._titta_errors('send the message'):
            self.experiment.tracker.send_message(str(self.var.message))
