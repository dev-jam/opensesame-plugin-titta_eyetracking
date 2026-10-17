"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
import os
from pathlib import Path
import pandas as pd


class TittaSaveData(Item):

    def reset(self):
        self.var.tsv_export = 'no'

    def prepare(self):
        super().prepare()
        self._init_var()
        self._check_init()

    def run(self):
        self._check_stop()
        self.set_item_onset()
        # Titta adds _1, _2, ... to the file name when a .h5 file with that
        # name (the part before the first dot) exists; choose the free name
        # the same way here, to export the data from the right file
        folder, base = os.path.split(self.experiment.titta_file_name)
        taken = {path.name.split('.')[0] for path in Path(folder or '.').glob('*.h5')}
        name = base
        i = 1
        while name in taken:
            name = f'{base}_{i}'
            i += 1
        file_name = os.path.join(folder, name)
        self.experiment.tracker.save_data(filename=name)

        if self.tsv_export == 'yes' and self.experiment.titta_dummy_mode == 'no':
            items_to_process = {
                'gaze': f'{file_name}_gaze.tsv',
                'msg': f'{file_name}_msg.tsv',
                'external_signal': f'{file_name}_external_signal.tsv',
                'calibration_history': f'{file_name}_calibration_history.tsv'
            }

            loaded_dfs = {}

            with pd.HDFStore(f'{file_name}.h5', 'r') as store:
                for item_name, output_file in items_to_process.items():
                    if f'/{item_name}' in store.keys():
                        loaded_dfs[item_name] = pd.read_hdf(store, item_name)
                        loaded_dfs[item_name].to_csv(output_file, sep='\t')
                        self._show_message(f"Saved {item_name} to {output_file}")
                    else:
                        self._show_message(f"Warning: '{item_name}' not found in HDF5 file")

            merge_candidates = [loaded_dfs[key] for key in ['gaze', 'msg', 'external_signal']
                               if key in loaded_dfs]

            if merge_candidates:
                df_merged = pd.concat(merge_candidates)
                df_merged.sort_values("system_time_stamp", axis=0, ascending=True,
                                     inplace=True, na_position='last')
                df_merged.to_csv(f'{file_name}_data_merged.tsv', sep='\t')
                self._show_message("Saved merged data")
            else:
                self._show_message("Warning: No dataframes available to merge")

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

    def _init_var(self):
        self.tsv_export = self.var.tsv_export

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaSaveData(TittaSaveData, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaSaveData.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

