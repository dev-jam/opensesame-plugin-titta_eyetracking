"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
import os


class TittaInit(Item):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'
        self.var.tracker = 'Tobii Pro Spectrum'
        self.var.bimonocular_calibration = 'no'
        self.var.ncalibration_targets = '5'
        self.var.eyeimage = 'no'
        self.var.operator = 'no'
        self.var.screen_name = 'default'
        self.var.screen_nr = 1
        self.var.xres = '1920'
        self.var.yres = '1080'
        self.var.waitblanking = 'no'

    def prepare(self):
        super().prepare()
        self._init_var()
        self._check_init()

        try:
            from titta import Titta
        except Exception:
            raise OSException('Could not import titta')

        if self.var.canvas_backend != 'psycho':
            raise OSException('Titta only supports PsychoPy as backend')
        self.file_name = 'subject-' + str(self.var.subject_nr)
        self.experiment.titta_file_name = os.path.normpath(os.path.join(os.path.dirname(self.var.logfile), self.file_name))
        self._show_message('Data will be stored in: %s' % self.file_name)

        self.settings = Titta.get_defaults(self.var.tracker)
        self.settings.FILENAME = self.file_name
        self.settings.DATA_STORAGE_PATH = os.path.dirname(self.var.logfile)
        self.settings.N_CAL_TARGETS = self.var.ncalibration_targets
        self.settings.DEBUG = False

        if self.var.operator == 'yes':
            # Monitor/geometry operator screen
            MY_MONITOR_OP                  = self.var.screen_name # needs to exists in PsychoPy monitor center
            FULLSCREEN_OP                  = False
            SCREEN_RES_OP                  = [self.var.xres, self.var.yres]
            SCREEN_WIDTH_OP                = 52.7 # cm
            VIEWING_DIST_OP                = 63 #  # distance from eye to center of screen (cm)

            from psychopy import visual, monitors

            mon_op = monitors.Monitor(MY_MONITOR_OP)  # Defined in defaults file
            mon_op.setWidth(SCREEN_WIDTH_OP)          # Width of screen (cm)
            mon_op.setDistance(VIEWING_DIST_OP)       # Distance eye / monitor (cm)
            mon_op.setSizePix(SCREEN_RES_OP)

            self.experiment.window_op = visual.Window(monitor = mon_op,
                                                      fullscr = FULLSCREEN_OP,
                                                      screen=self.var.screen_nr,
                                                      size=SCREEN_RES_OP,
                                                      units = 'norm',
                                                      waitBlanking=self.experiment.titta_operator_waitblanking)
            self.experiment.cleanup_functions.append(self.experiment.window_op.close)

        self._show_message('Initialising Eye Tracker')
        self.set_item_onset()
        self.experiment.tracker = Titta.Connect(self.settings)
        if self.var.dummy_mode == 'yes':
            self._show_message('Dummy mode activated')
            self.experiment.tracker.set_dummy_mode()
        self.experiment.tracker.init()

    def _check_init(self):
        if hasattr(self.experiment, 'tracker'):
            raise OSException('You should have only one instance of `titta_init` in your experiment')

    def _init_var(self):
        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.titta_recording = None
        self.experiment.titta_dummy_mode = self.var.dummy_mode
        self.experiment.titta_verbose = self.var.verbose
        self.experiment.titta_bimonocular_calibration = self.var.bimonocular_calibration
        if self.var.eye_image == 'yes':
            self.experiment.titta_eye_image = True
        else:
            self.experiment.titta_eye_image = False
        self.experiment.titta_operator = self.var.operator
        self.experiment.titta_operator_xres = self.var.xres
        self.experiment.titta_operator_yres = self.var.yres
        self.experiment.titta_operator_screen_nr = self.var.screen_nr
        self.experiment.titta_operator_screen_name = self.var.screen_name
        if self.var.waitblanking == 'no':
            self.experiment.titta_operator_waitblanking = False
        else:
            self.experiment.titta_operator_waitblanking = True

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtTittaInit(TittaInit, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TittaInit.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.line_edit_xres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_yres.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_nr.setEnabled(self.checkbox_operator.isChecked())
        self.line_edit_screen_name.setEnabled(self.checkbox_operator.isChecked())
        self.checkbox_waitblanking.setEnabled(self.checkbox_operator.isChecked())
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_xres.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_yres.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_screen_nr.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.line_edit_screen_name.setEnabled)
        self.checkbox_operator.stateChanged.connect(
            self.checkbox_waitblanking.setEnabled)
