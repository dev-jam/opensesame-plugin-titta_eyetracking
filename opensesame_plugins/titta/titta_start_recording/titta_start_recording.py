"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class TittaStartRecording(Item):

    def prepare(self):
        super().prepare()
        self._check_init()
        self.experiment.titta_start_recording = True

    def run(self):
        self._check_stop()
        self.set_item_onset()
        self.experiment.tracker.start_recording(gaze=True,
                                                time_sync=True,
                                                eye_image=False,
                                                notifications=True,
                                                external_signal=True,
                                                positioning=True)
        self.experiment.titta_recording = True

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise OSException('You should have one instance of `Titta Init` at the start of your experiment')

    def _check_stop(self):
        if not hasattr(self.experiment, "titta_stop_recording"):
            raise OSException(
                    '`Titta Stop Recording` item is missing')
        else:
            if self.experiment.titta_recording:
                raise OSException(
                        'Titta still recording, you first have to stop recording before starting')
        
    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaStartRecording(TittaStartRecording, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaStartRecording.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

