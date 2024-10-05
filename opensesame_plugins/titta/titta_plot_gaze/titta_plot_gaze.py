"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
import math


class TittaPlotGaze(Item):

    def reset(self):
        self.var.stimulus_display = 'no'
        self.var.operator_display = 'no'
        self.var.simulate_gaze = 'no'
        self.var.disable_waitblanking_gaze  = 'no'
        self.var.response_key = ''
        self.var.timeout = 'infinite'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

        if self.var.response_key != '':
            self._allowed_responses = []
            for r in safe_decode(self.var.response_key).split(';'):
                if r.strip() != '':
                    self._allowed_responses.append(r)
            if not self._allowed_responses:
                self._allowed_responses = None
            self._show_message("Response key(s) set to %s" % self._allowed_responses)

        if isinstance(self.var.timeout, int):
            if self.var.timeout > 0:
                self.timeout = self.var.timeout
            else:
                raise OSException('Timeout can not be negative')
        elif isinstance(self.var.timeout, str):
            if self.var.timeout == 'infinite':
                self.timeout = self.var.timeout
            else:
                raise OSException('Timeout can only be "infinite" or a positive integer')
        else:
            raise OSException('Timeout can only be "infinite" or a positive integer')

    def run(self):

        from psychopy import visual

        self.kb = Keyboard(self.experiment, timeout=1)
        self.kb.keylist = self._allowed_responses
        self.kb.flush()

        rel = self.experiment.var.width/self.experiment.var.height
        rad = 0.02

        image_stim = self.experiment.window._getFrame()

        if self.operator_display and self.experiment.titta_operator_waitblanking and self.disable_waitblanking_gaze:
            self.experiment.window_op.waitBlanking = False

        if self.stimulus_display:
            image = visual.ImageStim(self.experiment.window, image=image_stim, units='norm', size=(2, 2))
            dot = visual.Circle(self.experiment.window, radius=(rad, rel*rad), units='norm', lineColor='blue', fillColor='blue', opacity=0.5)
        if self.operator_display:
            image_op = visual.ImageStim(self.experiment.window_op, image=image_stim, units='norm', size=(2, 2))
            dot_op = visual.Circle(self.experiment.window_op, radius=(rad, rel*rad), units='norm', lineColor='blue', fillColor='blue', opacity=0.5)

        counter = 1
        items = 60
        key = None
        time = None
        self.debug = False

        self.start_time = self.set_item_onset()

        while not key:

            if self.timeout != 'infinite':
                if self.clock.time() - self.start_time >= self.var.timeout:
                    break

            if (self.stimulus_display or self.operator_display) and (self.experiment.titta_dummy_mode == 'no' or self.simulate):

                if self.debug:
                    t0 = self.clock.time()

                if self.experiment.titta_dummy_mode == 'no':
                    sample = self.experiment.tracker.buffer.peek_N('gaze', 1)

                    L_X = sample['left_gaze_point_on_display_area_x'][0] * 2 - 1
                    L_Y = 1 - sample['left_gaze_point_on_display_area_y'][0] * 2
                    R_X = sample['right_gaze_point_on_display_area_x'][0] * 2 - 1
                    R_Y = 1 - sample['right_gaze_point_on_display_area_y'][0] * 2

                elif self.simulate:
                    r = 0.050
                    L = -0.020
                    R = 0.120

                    L_X = L + r * math.cos(2 * math.pi * counter / items)
                    L_Y = r * math.sin(2 * math.pi * counter / items)

                    R_X = R + r * math.cos(2 * math.pi * counter / items);
                    R_Y = r * math.sin(2 * math.pi * counter / items);

                    counter += 1

                if self.debug:
                    t1 = self.clock.time()
                    self._show_message('')
                    self._show_message('Process sample duration: %s ms' % (str(round(t1-t0, 1))))

                if self.stimulus_display:
                    image.draw()

                    dot.lineColor = 'red'
                    dot.fillColor = 'red'
                    dot.pos = (L_X, L_Y)
                    dot.draw()

                    dot.lineColor = 'blue'
                    dot.fillColor = 'blue'
                    dot.pos = (R_X, R_Y)
                    dot.draw()

                    #self.experiment.window.flip()

                if self.debug:
                    t2 = self.clock.time()
                    self._show_message('Draw stim duration: %s ms' % (str(round(t2-t1, 1))))

                if self.operator_display:
                    image_op.draw()

                    dot_op.lineColor = 'red'
                    dot_op.fillColor = 'red'
                    dot_op.pos = (L_X, L_Y)
                    dot_op.draw()

                    dot_op.lineColor = 'blue'
                    dot_op.fillColor = 'blue'
                    dot_op.pos = (R_X, R_Y)
                    dot_op.draw()

                    #self.experiment.window_op.flip()

                if self.debug:
                    t3 = self.clock.time()
                    self._show_message('Draw operator duration: %s ms' % (str(round(t3-t2, 1))))

                self._flip_windows()

            key, time = self.kb.get_key()

        self._set_response_time()
        response_time = round(time - self.start_time, 1)
        self._show_message("Detected press on button: '%s'" % key)
        self._show_message("Response time: %s ms" % response_time)

        if self.operator_display and self.experiment.titta_operator_waitblanking and self.disable_waitblanking_gaze:
            self.experiment.window_op.waitBlanking = self.experiment.titta_operator_waitblanking

    def _flip_windows(self):
        if self.debug:
            t0 = self.clock.time()
        if self.operator_display:
            self.experiment.window_op.flip()
        if self.debug:
            t1 = self.clock.time()
            self._show_message('Flip operator duration: %s ms' % (str(round(t1-t0, 1))))
        if self.stimulus_display:
            self.experiment.window.flip()
        if self.debug:
            t2 = self.clock.time()
            self._show_message('Flip stim duration: %s ms' % (str(round(t2-t1, 1))))
            self._show_message('Flip total duration: %s ms' % (str(round(t2-t0, 1))))
            self._show_message('')

    def _init_var(self):
        if self.var.stimulus_display == 'yes':
            self.stimulus_display = True
        else:
            self.stimulus_display = False

        if self.var.operator_display == 'yes' and self.experiment.titta_operator == 'no':
            self.operator_display = False
            raise OSException('Operator screen selected but not enabled in the `titta_init` item')
        elif self.var.operator_display == 'yes' and self.experiment.titta_operator == 'yes':
            self.operator_display = True
        else:
            self.operator_display = False

        if self.var.disable_waitblanking_gaze  == 'no':
            self.disable_waitblanking_gaze = False
        else:
            self.disable_waitblanking_gaze = True

        if self.var.simulate_gaze == 'no':
            self.simulate = False
        else:
            self.simulate = True

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise OSException('You should have one instance of `titta_init` at the start of your experiment')

    def _set_response_time(self, time=None):
        if time is None:
            time = self.clock.time()
        self.experiment.var.set('time_response_%s' % self.name, time)
        return time

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaPlotGaze(TittaPlotGaze, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaPlotGaze.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    # def init_edit_widget(self):
    #     super().init_edit_widget()
    #     self.checkbox_disable_waitblanking_gaze.setEnabled(self.checkbox_operator_display.isChecked())
    #     self.checkbox_operator_display.stateChanged.connect(
    #         self.checkbox_disable_waitblanking_gaze.setEnabled)
