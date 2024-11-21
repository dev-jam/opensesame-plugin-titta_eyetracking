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

    def reset(self):
        self.var.start_gaze = 'yes'
        self.var.start_time_sync = 'yes'
        self.var.start_eye_image = 'no'
        self.var.start_notifications = 'yes'
        self.var.start_external_signal = 'yes'
        self.var.start_positioning = 'yes'
        self.var.blocking_mode = 'yes'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()
        self.experiment.titta_start_recording = True

    def run(self):
        self._check_stop()
        self.set_item_onset()
        self.experiment.tracker.start_recording(gaze=self.start_gaze,
                                                time_sync=self.start_time_sync,
                                                eye_image=self.start_eye_image,
                                                notifications=self.start_notifications,
                                                external_signal=self.start_external_signal,
                                                positioning=self.start_positioning,
                                                block_until_data_available=self.blocking_mode)
        self.experiment.titta_recording = True

    def _init_var(self):
        if self.var.blocking_mode == 'yes':
            self.blocking_mode = True
        else:
            self.blocking_mode = False
        if self.var.start_gaze == 'yes':
            self.start_gaze = True
        else:
            self.start_gaze = False
        if self.var.start_time_sync == 'yes':
            self.start_time_sync = True
        else:
            self.start_time_sync = False
        if self.var.start_eye_image == 'yes':
            self.start_eye_image = True
        else:
            self.start_eye_image = False
        if self.var.start_notifications == 'yes':
            self.start_notifications = True
        else:
            self.start_notifications = False
        if self.var.start_external_signal == 'yes':
            self.start_external_signal = True
        else:
            self.start_external_signal = False
        if self.var.start_positioning == 'yes':
            self.start_positioning = True
        else:
            self.start_positioning = False

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

