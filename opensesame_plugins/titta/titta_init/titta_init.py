"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
import os


class TittaInit(Item):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'
        self.var.tracker = 'Tobii Pro Spectrum'
        self.var.bimonocular_calibration = 'no'
        self.var.ncalibration_targets = '5'

    def prepare(self):
        super().prepare()
        self._init_var()
        self._check_init()

        try:
            from titta import Titta
        except Exception:
            raise OSException('Could not import titta')

        if self.var.canvas_backend != 'psycho':
            raise OSException('Titta only supports PsychoPy as backend')
        self.file_name = 'subject-' + str(self.var.subject_nr)
        self._show_message('Data will be stored in: %s' % self.file_name)

        self.settings = Titta.get_defaults(self.var.tracker)
        self.settings.FILENAME = self.file_name
        self.settings.DATA_STORAGE_PATH = os.path.dirname(self.var.logfile)
        self.settings.N_CAL_TARGETS = self.var.ncalibration_targets
        self.settings.DEBUG = False

        self._show_message('Initialising Eye Tracker')
        self.set_item_onset()
        self.experiment.tracker = Titta.Connect(self.settings)
        if self.var.dummy_mode == 'yes':
            self._show_message('Dummy mode activated')
            self.experiment.tracker.set_dummy_mode()
        self.experiment.tracker.init()

    def _check_init(self):
        if hasattr(self.experiment, 'tracker'):
            raise OSException('You should have only one instance of `titta_init` in your experiment')

    def _init_var(self):
        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.titta_recording = None
        self.experiment.titta_dummy_mode = self.var.dummy_mode
        self.experiment.titta_verbose = self.var.verbose
        self.experiment.titta_bimonocular_calibration = self.var.bimonocular_calibration

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaInit(TittaInit, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaInit.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
