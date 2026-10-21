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

from contextlib import contextmanager

from libopensesame.item import Item
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

# Streams that the start/stop recording items switch on and off; the
# `start_<stream>` and `stop_<stream>` variables hold the settings
STREAMS = ('gaze', 'time_sync', 'eye_image', 'notifications',
           'external_signal', 'positioning')


class TittaItem(Item):
    """Base class of the Titta items. The `titta_init` item stores the shared
    state on the experiment; the other items read it in `_check_init()`.
    """

    def _check_init(self):
        if not hasattr(self.experiment, 'titta_dummy_mode'):
            raise OSException('You should have one instance of `Titta Init` at the start of your experiment')
        self.dummy_mode = self.experiment.titta_dummy_mode == 'yes'
        self.verbose = self.experiment.titta_verbose == 'yes'

    def _check_not_recording(self, action):
        if not hasattr(self.experiment, 'titta_stop_recording'):
            raise OSException('`Titta Stop Recording` item is missing')
        if self.experiment.titta_recording:
            raise OSException(f'Titta still recording, you first have to stop recording before {action}')

    def _stop_dummy_buffer(self):
        # In dummy mode, Titta's calibrate() starts a thread that simulates
        # gaze with the mouse and never stops it; a running thread keeps the
        # experiment from ending. _stop_sample_buffer() is private Titta API.
        buffer = getattr(self.experiment.tracker, 'buffer', None)
        if buffer is not None:
            buffer._stop_sample_buffer()

    @contextmanager
    def _titta_errors(self, action):
        # Titta raises plain exceptions (e.g. eye tracker not found); the
        # experiment would only show "An unexpected error occurred"
        try:
            yield
        except OSException:
            raise
        except Exception as e:
            message = ' '.join(str(e).split()) or type(e).__name__
            raise OSException(f'Titta could not {action}: {message}') from e

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)
