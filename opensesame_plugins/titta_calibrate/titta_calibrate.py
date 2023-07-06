#-*- coding:utf-8 -*-
"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception
from libopensesame import debug


class titta_calibrate(item):

    # Provide an informative description for your plug-in.
    description = 'Titta item to start calibration'

    def reset(self):
        """Resets plug-in to initial values."""
        pass

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        item.prepare(self)
        self._check_init()

    def run(self):
        """The run phase of the plug-in goes here."""
        from titta import helpers_tobii
        self.fixation_point = helpers_tobii.MyDot2(self.experiment.window)

        self._show_message('Starting calibration')
        self.set_item_onset()
        #  Calibrate
        if self.experiment.titta_bimonocular_calibration == 'yes':
            self.experiment.tracker.calibrate(self.experiment.window, eye='left', calibration_number='first')
            self.experiment.tracker.calibrate(self.experiment.window, eye='right', calibration_number='second')
        elif self.experiment.titta_bimonocular_calibration == 'no':
            self.experiment.tracker.calibrate(self.experiment.window)

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise osexception(
                    u'You should have one instance of `titta_init` at the start of your experiment')

    def _show_message(self, message):
        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qttitta_calibrate(titta_calibrate, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""

    def __init__(self, name, experiment, script=None):
        titta_calibrate.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
