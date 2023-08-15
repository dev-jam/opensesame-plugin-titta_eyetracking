"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class TittaSendMessage(Item):

    def reset(self):
        self.var.message = 'onset_stimulusname'

    def prepare(self):
        super().prepare()
        self._check_init()

    def run(self):
        self.set_item_onset()
        self.experiment.tracker.send_message(self.var.message)

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


class QtTittaSendMessage(TittaSendMessage, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaSendMessage.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
