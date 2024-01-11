"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
import pandas as pd


class TittaSaveData(Item):

    def prepare(self):
        super().prepare()
        self._check_init()

    def run(self):
        self._check_stop()
        self.set_item_onset()
        self.experiment.tracker.save_data()

        # save data as tsv file
        df_gaze = pd.read_hdf(self.experiment.titta_file_name + '.h5', 'gaze')
        df_msg = pd.read_hdf(self.experiment.titta_file_name + '.h5', 'msg')
        df_gaze.to_csv(self.experiment.titta_file_name + '_gaze.tsv', sep='\t')
        df_msg.to_csv(self.experiment.titta_file_name + '_msg.tsv', sep='\t')

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
        elif self.experiment.titta_recording:
                raise OSException(
                        'Titta still recording, you first have to stop recording before saving data')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaSaveData(TittaSaveData, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaSaveData.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

