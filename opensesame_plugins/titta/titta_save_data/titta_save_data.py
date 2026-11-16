"""
This file is part of opensesame-plugin-titta_eyetracking.

Copyright (C) 2023-2026 Bob Rosbag <mail@bobrosbag.nl>, Diederick C. Niehorster, Marcus Nyström

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

__author__ = "Bob Rosbag"
__license__ = "GPL-3.0-or-later"

import os
from datetime import datetime
from pathlib import Path

import h5py
import pandas as pd
from PIL import Image
from libopensesame.oslogging import oslogger

from ..titta_item import TittaItem

# Data that Titta always saves, or saves with the external signal stream;
# a warning when one of them is missing. All pandas tables in the HDF5
# file are exported, also the ones not listed here (e.g. time_sync,
# notification, eye_metadata, log)
TSV_EXPECTED = ('gaze', 'msg', 'external_signal', 'calibration_history')
# Group in the HDF5 file with one dataset per eye image (Titta writes it
# with h5py; dataset <k> belongs to row <k> of eye_metadata)
EYE_IMAGE_GROUP = 'eye_image'


class TittaSaveData(TittaItem):

    def reset(self):
        self.var.tsv_export = 'no'
        self.var.png_export = 'no'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        self._check_not_recording('saving data')
        self.set_item_onset()
        file_name = self._free_file_name()
        with self._titta_errors('save the data'):
            self.experiment.tracker.save_data(filename=os.path.basename(file_name))
        if self.dummy_mode:
            return
        if self.tsv_export:
            self._export('tsv', self._export_tsv, file_name)
        if self.png_export:
            self._export('png', self._export_eye_images, file_name)

    def _init_var(self):
        self.tsv_export = self.var.tsv_export == 'yes'
        self.png_export = self.var.png_export == 'yes'

    def _export(self, kind, export, file_name):
        # An export must never end the experiment: Titta has already written
        # the .h5 file, and the items after this one (e.g. a logger) must
        # still run. A failure is a warning in the log instead
        try:
            export(file_name)
        except Exception as e:
            oslogger.warning(f'{kind} export of {file_name}.h5 failed, '
                             f'the experiment continues: {e!r}')

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
        with pd.HDFStore(f'{file_name}.h5', 'r') as store:
            keys = [key.lstrip('/') for key in store.keys()]
            for key in TSV_EXPECTED:
                if key not in keys:
                    oslogger.warning(f"'{key}' not found in HDF5 file")
            for key in keys:
                # One table that fails doesn't stop the export of the others
                output_file = f'{file_name}_{key.replace("/", "_")}.tsv'
                try:
                    pd.read_hdf(store, key).to_csv(output_file, sep='\t')
                except Exception as e:
                    oslogger.warning(f"tsv export of '{key}' to {output_file} failed: {e!r}")
                    continue
                self._show_message(f'Saved {key} to {output_file}')

    def _export_eye_images(self, file_name):
        # Each eye image becomes <file_name>_eye_image/<k>.png
        with h5py.File(f'{file_name}.h5', 'r') as hf:
            if EYE_IMAGE_GROUP not in hf:
                # Eye images are only recorded when asked for: not an error
                self._show_message('No eye images in the HDF5 file, no png export')
                return
            group = hf[EYE_IMAGE_GROUP]
            folder = self._free_folder_name(f'{file_name}_{EYE_IMAGE_GROUP}')
            os.makedirs(folder)
            saved = 0
            failed = []
            for name, dataset in group.items():
                # One image that fails doesn't stop the export of the others;
                # one warning for all failures
                output_file = os.path.join(folder, f'{name}.png')
                try:
                    Image.fromarray(dataset[()]).save(output_file)
                except Exception as e:
                    failed.append((name, e))
                    continue
                saved += 1
            if failed:
                name, e = failed[0]
                oslogger.warning(f'png export: {len(failed)} of {len(group)} eye images '
                                 f'failed, the first ({name}): {e!r}')
            self._show_message(f'Saved {saved} eye images to {folder}')

    def _free_folder_name(self, folder):
        # Never write into an existing folder (e.g. left by an earlier run
        # whose .h5 file was moved): add the date and time, and a number
        # when that exists too
        if not os.path.exists(folder):
            return folder
        stamped = f'{folder}_{datetime.now():%Y%m%d-%H%M%S}'
        name = stamped
        i = 1
        while os.path.exists(name):
            name = f'{stamped}_{i}'
            i += 1
        oslogger.warning(f'png export: {folder} exists, the eye images go to {name}')
        return name
