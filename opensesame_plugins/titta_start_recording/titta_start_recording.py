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


class titta_start_recording(item):

    # Provide an informative description for your plug-in.
    description = 'Titta item to start recording'

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
        self.experiment.tracker.start_recording(gaze=True,
                                time_sync=True,
                                eye_image=False,
                                notifications=True,
                                external_signal=True,
                                positioning=True)

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


class qttitta_start_recording(titta_start_recording, qtautoplugin):
    """This class handles the GUI aspect of the plug-in."""
    
    def __init__(self, name, experiment, script=None):
        titta_start_recording.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)