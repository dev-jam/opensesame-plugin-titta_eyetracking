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

from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class QtTittaItem(QtAutoPlugin):
    """GUI base class of the Titta items. Enables controls only while their
    checkbox is checked; subclasses list them in `dependent_controls`.
    """

    # {checkbox name: [names of the controls it enables]}
    dependent_controls = {}

    def __init__(self, plugin_file):
        super().__init__(plugin_file)
        self._need_to_connect = True

    def auto_edit_widget(self):
        super().auto_edit_widget()
        if not self._need_to_connect:
            return
        self._need_to_connect = False
        for checkbox, controls in self.dependent_controls.items():
            for control in controls:
                getattr(self, checkbox).toggled.connect(
                    getattr(self, control).setEnabled)

    def edit_widget(self):
        widget = super().edit_widget()
        # auto_edit_widget() enables the checkboxes and comboboxes again on
        # each refresh, so set the state here
        for checkbox, controls in self.dependent_controls.items():
            for control in controls:
                getattr(self, control).setEnabled(
                    getattr(self, checkbox).isChecked())
        return widget
