#-*- coding:utf-8 -*-
"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin


class titta_send_message(item):

    # Provide an informative description for your plug-in.
    description = 'An example new-style plug-in'

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.message = 'Default text'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        item.prepare(self)

    def run(self):
        """The run phase of the plug-in goes here."""
        self.experiment.tracker.send_message(self.var.message)


class qttitta_send_message(titta_send_message, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""
    
    def __init__(self, name, experiment, script=None):
        titta_send_message.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)