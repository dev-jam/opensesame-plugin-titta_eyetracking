"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class TittaStopRecording(Item):

    def reset(self):
        self.var.stop_gaze = 'yes'
        self.var.stop_time_sync = 'yes'
        self.var.stop_eye_image = 'no'
        self.var.stop_notifications = 'yes'
        self.var.stop_external_signal = 'yes'
        self.var.stop_positioning = 'yes'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()
        self.experiment.titta_stop_recording = True

    def run(self):
        self._check_start()
        self.set_item_onset()
        self.experiment.tracker.stop_recording(gaze=self.stop_gaze,
                                               time_sync=self.stop_time_sync,
                                               eye_image=self.stop_eye_image,
                                               notifications=self.stop_notifications,
                                               external_signal=self.stop_external_signal,
                                               positioning=self.stop_positioning)
        self.experiment.titta_recording = False

    def _init_var(self):
        self.stop_gaze = self._make_boolean(self.var.stop_gaze)
        self.stop_time_sync = self._make_boolean(self.var.stop_time_sync)
        self.stop_eye_image = self._make_boolean(self.var.stop_eye_image)
        self.stop_notifications = self._make_boolean(self.var.stop_notifications)
        self.stop_external_signal = self._make_boolean(self.var.stop_external_signal)
        self.stop_positioning = self._make_boolean(self.var.stop_positioning)

    def _check_init(self):
        if hasattr(self.experiment, "titta_dummy_mode"):
            self.dummy_mode = self.experiment.titta_dummy_mode
            self.verbose = self.experiment.titta_verbose
        else:
            raise OSException('You should have one instance of `Titta Init` at the start of your experiment')

    def _check_start(self):
        if not hasattr(self.experiment, "titta_start_recording"):
            raise OSException(
                    '`Titta Start Recording` item is missing')
        else:
            if not self.experiment.titta_recording:
                raise OSException(
                        'Titta not recording, you first have to start recording before stopping')

    def _make_boolean(self, var):
        if var == 'yes':
            return True
        elif var == 'no':
            return False
        else:
            raise OSException(
                    '`Variable` is not `yes` or `no`')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaStopRecording(TittaStopRecording, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaStopRecording.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

