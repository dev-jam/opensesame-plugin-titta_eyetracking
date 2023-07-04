#-*- coding:utf-8 -*-
"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin


class titta_calibrate(item):

    # Provide an informative description for your plug-in.
    description = 'An example new-style plug-in'

    def reset(self):
        """Resets plug-in to initial values."""
        pass

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        item.prepare(self)

    def run(self):
        """The run phase of the plug-in goes here."""
        from titta import helpers_tobii
        self.fixation_point = helpers_tobii.MyDot2(self.experiment.window)
        
        #  Calibrate
        if self.experiment.titta_bimonocular_calibration == 'yes':
            self.experiment.tracker.calibrate(self.experiment.window, eye='left', calibration_number='first')
            self.experiment.tracker.calibrate(self.experiment.window, eye='right', calibration_number='second')
        elif self.experiment.titta_bimonocular_calibration == 'no':
            self.experiment.tracker.calibrate(self.experiment.window)


class qttitta_calibrate(titta_calibrate, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""
    
    def __init__(self, name, experiment, script=None):
        titta_calibrate.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
