#-*- coding:utf-8 -*-
"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import os

class titta_init(item):

    # Provide an informative description for your plug-in.
    description = 'An example new-style plug-in'

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.dummy_mode = 'no'  # yes = checked, no = unchecked
        self.var.tracker = 'Tobii Pro Spectrum'
        self.var.bimonocular_calibration = 'no'
        self.var.ncalibration_targets = '3'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        item.prepare(self)
        
        self.experiment.titta_bimonocular_calibration = self.var.bimonocular_calibration
        
        try:
            from titta import Titta
        except:
            print('Could not import titta')
        
        self.file_name = 'subject-' + str(self.experiment.subject_nr) + '_TOBII_output.hd5'
        
        if self.experiment.experiment_path:
            self.fname = self.experiment.experiment_path + os.sep + self.file_name
        else:
            self.fname = self.file_name
        
        print('Data will be stored in: %s' % self.fname)
        
        self.settings = Titta.get_defaults(self.var.tracker)
        self.settings.FILENAME = self.fname
        self.settings.N_CAL_TARGETS = self.var.ncalibration_targets
        self.settings.DEBUG = False
        
        # %% Connect to eye tracker and calibrate
        self.experiment.tracker = Titta.Connect(self.settings)
        if self.var.dummy_mode == 'yes':
             print('Dummy mode activated')
             self.experiment.tracker.set_dummy_mode()
        self.experiment.tracker.init()

    def run(self):
        """The run phase of the plug-in goes here."""
        pass


class qttitta_init(titta_init, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""
    
    def __init__(self, name, experiment, script=None):
        titta_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
