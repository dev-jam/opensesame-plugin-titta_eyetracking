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

import os
from pathlib import Path

import pandas as pd
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

from ..titta_item import TittaItem

# Data in the HDF5 file that is exported to tsv files
TSV_EXPORT = ('gaze', 'msg', 'external_signal', 'calibration_history')
# Data that is also merged into one tsv file, sorted by time
TSV_MERGE = ('gaze', 'msg', 'external_signal')


class TittaSaveData(TittaItem):

    def reset(self):
        self.var.tsv_export = 'no'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        self._check_stop()
        self.set_item_onset()
        file_name = self._free_file_name()
        self.experiment.tracker.save_data(filename=os.path.basename(file_name))
        if self.tsv_export and not self.dummy_mode:
            self._export_tsv(file_name)

    def _init_var(self):
        self.tsv_export = self.var.tsv_export == 'yes'

    def _free_file_name(self):
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
        return os.path.join(folder, name)

    def _export_tsv(self, file_name):
        data = {}
        with pd.HDFStore(f'{file_name}.h5', 'r') as store:
            for key in TSV_EXPORT:
                if f'/{key}' not in store.keys():
                    oslogger.warning(f"'{key}' not found in HDF5 file")
                    continue
                data[key] = pd.read_hdf(store, key)
                output_file = f'{file_name}_{key}.tsv'
                data[key].to_csv(output_file, sep='\t')
                self._show_message(f'Saved {key} to {output_file}')

        merge = [data[key] for key in TSV_MERGE if key in data]
        if not merge:
            oslogger.warning('No data available to merge')
            return
        merged = pd.concat(merge).sort_values('system_time_stamp', na_position='last')
        merged.to_csv(f'{file_name}_data_merged.tsv', sep='\t')
        self._show_message('Saved merged data')

    def _check_stop(self):
        if not hasattr(self.experiment, 'titta_stop_recording'):
            raise OSException('`Titta Stop Recording` item is missing')
        if self.experiment.titta_recording:
            raise OSException('Titta still recording, you first have to stop recording before saving data')
