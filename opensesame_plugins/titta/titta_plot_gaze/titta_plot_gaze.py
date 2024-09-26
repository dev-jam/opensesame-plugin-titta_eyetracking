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
import numpy as np


class TittaPlotGaze(Item):

    def reset(self):
        self.var.response_key = ''
        self.var.timeout = 'infinite'

    def prepare(self):
        super().prepare()
        self._check_init()

        if self.var.response_key != '':
            self._allowed_responses = []
            for r in safe_decode(self.var.response_key).split(';'):
                if r.strip() != '':
                    self._allowed_responses.append(r)
            if not self._allowed_responses:
                self._allowed_responses = None
            self._show_message("Response key(s) set to %s" % self._allowed_responses)

    def run(self):
        
        from psychopy import visual

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

        self.kb = Keyboard(self.experiment, timeout=1)
        self.kb.keylist = self._allowed_responses
        self.kb.flush()
        key = None
        
        rel = self.experiment.var.width/self.experiment.var.height
        rad = 0.02
        
        image_stim = self.experiment.window.getMovieFrame()
        if self.experiment.titta_operator == 'no':
            image = visual.ImageStim(self.experiment.window, image=image_stim, units='norm', size=(2, 2))
            dot = visual.Circle(self.experiment.window, radius=(rad, rel*rad), units='norm', lineColor='red', fillColor='red', opacity=0.5)
        elif self.experiment.titta_operator == 'yes':
            image = visual.ImageStim(self.experiment.window_op, image=image_stim, units='norm', size=(2, 2))
            dot = visual.Circle(self.experiment.window_op, radius=(rad, rel*rad), units='norm', lineColor='red', fillColor='red', opacity=0.5)
        
        counter = 1
        
        self.start_time = self.set_item_onset()
        
        while not key:
            
            if self.timeout != 'infinite':
                if self.clock.time() - self.start_time >= self.var.timeout:
                    break
            
            image.draw()
            
            if self.experiment.titta_dummy_mode == 'no':
                sample = self.experiment.tracker.buffer.peek_N('gaze', 1) 
        
                L_X = sample['left_gaze_point_on_display_area_x'][0] * 2 - 1
                L_Y = 1 - sample['left_gaze_point_on_display_area_y'][0] * 2
                R_X = sample['right_gaze_point_on_display_area_x'][0] * 2 - 1
                R_Y = 1 - sample['right_gaze_point_on_display_area_y'][0] * 2
            
                dot.lineColor = 'red'
                dot.fillColor = 'red'
                dot.pos = (L_X, L_Y)
                dot.draw()
                
                dot.lineColor = 'blue'
                dot.fillColor = 'blue'
                dot.pos = (R_X, R_Y)
                dot.draw()
            else:
                dot.lineColor = 'red'
                dot.fillColor = 'red'
                dot.pos = ((-5+counter)/1000, (-5+counter)/1000)
                dot.draw()
                
                dot.lineColor = 'blue'
                dot.fillColor = 'blue'
                dot.pos = ((5+counter)/1000, (5+counter)/1000)
                dot.draw()
                counter += 1

            if self.experiment.titta_operator == 'no':
                self.experiment.window.flip()
            elif self.experiment.titta_operator == 'yes':
                self.experiment.window_op.flip()

            key, time = self.kb.get_key()

        self._set_response_time()
        response_time = round(time - self.start_time, 1)
        self._show_message("Detected press on button: '%s'" % key)
        self._show_message("Response time: %s ms" % response_time)

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
