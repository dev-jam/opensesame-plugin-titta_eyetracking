"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class TittaCalibrate(Item):

    def prepare(self):
        super().prepare()
        self._check_init()

    def run(self):
        from titta import helpers_tobii
        self.fixation_point = helpers_tobii.MyDot2(self.experiment.window)
        self._show_message('Starting calibration')
        self.set_item_onset()
        if self.experiment.titta_bimonocular_calibration == 'yes':
            self.experiment.tracker.calibrate(self.experiment.window, eye='left',
                                              calibration_number='first')
            self.experiment.tracker.calibrate(self.experiment.window, eye='right',
                                              calibration_number='second')
        elif self.experiment.titta_bimonocular_calibration == 'no':
            self.experiment.tracker.calibrate(self.experiment.window)

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise OSException('You should have one instance of `titta_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class qtTittaCalibrate(TittaCalibrate, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaCalibrate.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
