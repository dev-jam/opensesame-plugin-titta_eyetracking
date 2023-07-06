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


class titta_send_message(item):

    # Provide an informative description for your plug-in.
    description = 'Titta item to send a message to the Eye Tracker'

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.message = 'onset_stimulusname'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        item.prepare(self)
        self._check_init()

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset()
        self.experiment.tracker.send_message(self.var.message)

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


class qttitta_send_message(titta_send_message, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""

    def __init__(self, name, experiment, script=None):
        titta_send_message.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
