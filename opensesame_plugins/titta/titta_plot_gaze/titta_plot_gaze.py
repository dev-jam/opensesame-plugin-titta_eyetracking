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

import math

from libopensesame.exceptions import OSException
from openexp.keyboard import Keyboard

from ..qt_titta_item import QtTittaItem
from ..titta_item import TittaItem

DOT_RADIUS = 0.02  # norm units
# Simulated gaze in dummy mode: both eyes move in a circle (norm units)
SIMULATION_RADIUS = 0.05
SIMULATION_LEFT_X = -0.02
SIMULATION_RIGHT_X = 0.12
SIMULATION_STEPS = 60  # samples per circle


class TittaPlotGaze(TittaItem):

    def reset(self):
        self.var.stimulus_display = 'no'
        self.var.operator_display = 'no'
        self.var.simulate_gaze = 'no'
        self.var.disable_waitblanking_gaze = 'no'
        self.var.response_key = ''
        self.var.timeout = 'infinite'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        from psychopy import visual

        self.kb = Keyboard(self.experiment, timeout=1)
        self.kb.flush()

        # The current stimulus display is the background of the gaze plot
        image_stim = self.experiment.window._getFrame()
        aspect_ratio = self.experiment.var.width / self.experiment.var.height
        displays = []
        if self.stimulus_display:
            displays.append(self.experiment.window)
        if self.operator_display:
            displays.append(self.experiment.window_op)
        plots = [
            (visual.ImageStim(window, image=image_stim, units='norm', size=(2, 2)),
             visual.Circle(window, radius=(DOT_RADIUS, aspect_ratio * DOT_RADIUS),
                           units='norm', opacity=0.5))
            for window in displays
        ]
        plot = bool(plots) and (not self.dummy_mode or self.simulate_gaze)

        if self.disable_waitblanking_gaze:
            self.experiment.window_op.waitBlanking = False

        step = 1
        key = None
        start_time = timestamp = self.set_item_onset()
        while key is None:
            if self.timeout is not None and \
                    self.clock.time() - start_time >= self.timeout:
                break
            if plot:
                left, right = self._gaze(step)
                step += 1
                for image, dot in plots:
                    self._draw_gaze(image, dot, left, right)
                # The operator display first, as before
                for window in reversed(displays):
                    window.flip()
            # Pass the key list on each call: get_key() adds 'escape' to a
            # stored key list every time it is called
            key, timestamp = self.kb.get_key(keylist=self.response_keys)

        self._set_response_time()
        self._show_message(f"Detected press on button: '{key}'")
        self._show_message(f'Response time: {round(timestamp - start_time, 1)} ms')

        if self.disable_waitblanking_gaze:
            self.experiment.window_op.waitBlanking = True

    def _init_var(self):
        self.stimulus_display = self.var.stimulus_display == 'yes'
        self.operator_display = self.var.operator_display == 'yes'
        if self.operator_display and self.experiment.titta_operator != 'yes':
            raise OSException('Operator screen selected but not enabled in the `titta_init` item')
        self.simulate_gaze = self.var.simulate_gaze == 'yes'
        # Only needed when waitBlanking is enabled on the operator screen
        self.disable_waitblanking_gaze = self.operator_display and \
            self.experiment.titta_operator_waitblanking and \
            self.var.disable_waitblanking_gaze == 'yes'

        keys = [key.strip() for key in str(self.var.response_key).split(';')]
        self.response_keys = [key for key in keys if key] or None
        self._show_message(f'Response key(s) set to {self.response_keys}')

        timeout = self.var.timeout
        if timeout == 'infinite':
            self.timeout = None
        elif isinstance(timeout, int) and timeout > 0:
            self.timeout = timeout
        else:
            raise OSException('Timeout can only be "infinite" or a positive integer')

    def _gaze(self, step):
        """Returns the left and right gaze position in norm units."""
        if not self.dummy_mode:
            sample = self.experiment.tracker.buffer.peek_N('gaze', 1)
            return tuple(
                (sample[f'{eye}_gaze_point_on_display_area_x'][0] * 2 - 1,
                 1 - sample[f'{eye}_gaze_point_on_display_area_y'][0] * 2)
                for eye in ('left', 'right'))
        angle = 2 * math.pi * step / SIMULATION_STEPS
        dx = SIMULATION_RADIUS * math.cos(angle)
        dy = SIMULATION_RADIUS * math.sin(angle)
        return (SIMULATION_LEFT_X + dx, dy), (SIMULATION_RIGHT_X + dx, dy)

    @staticmethod
    def _draw_gaze(image, dot, left, right):
        image.draw()
        for color, pos in (('red', left), ('blue', right)):
            dot.lineColor = color
            dot.fillColor = color
            dot.pos = pos
            dot.draw()

    def _set_response_time(self):
        self.experiment.var.set(f'time_response_{self.name}', self.clock.time())


class QtTittaPlotGaze(TittaPlotGaze, QtTittaItem):

    dependent_controls = {
        'checkbox_operator_display': ['checkbox_disable_waitblanking_gaze'],
    }

    def __init__(self, name, experiment, script=None):
        TittaPlotGaze.__init__(self, name, experiment, script)
        QtTittaItem.__init__(self, __file__)
