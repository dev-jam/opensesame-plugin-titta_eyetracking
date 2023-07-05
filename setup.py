#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Bob Rosbag
2022

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from setuptools import setup


def get_readme():

    if os.path.exists('README.md'):
        with open('README.md') as fd:
            return fd.read()
    return 'No readme information'


setup(
    name='opensesame-plugin-titta_eyetracking',
    version='0.3.0',
    description='Titta Eye Tracking plugin for OpenSesame',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author='Bob Rosbag',
    author_email='debian@bobrosbag.nl',
    url='https://github.com/dev-jam/opensesame-plugin-titta_eyetracking',
    # Classifiers used by PyPi if you upload the plugin there
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    packages=[],
    data_files=[
        ('share/opensesame_plugins/titta_init',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/titta_init/titta_init.md',
            'opensesame_plugins/titta_init/titta_init.png',
            'opensesame_plugins/titta_init/titta_init_large.png',
            'opensesame_plugins/titta_init/titta_init.py',
            'opensesame_plugins/titta_init/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/titta_calibrate',
        [
            'opensesame_plugins/titta_calibrate/titta_calibrate.md',
            'opensesame_plugins/titta_calibrate/titta_calibrate.png',
            'opensesame_plugins/titta_calibrate/titta_calibrate_large.png',
            'opensesame_plugins/titta_calibrate/titta_calibrate.py',
            'opensesame_plugins/titta_calibrate/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/titta_send_message',
        [
            'opensesame_plugins/titta_send_message/titta_send_message.md',
            'opensesame_plugins/titta_send_message/titta_send_message.png',
            'opensesame_plugins/titta_send_message/titta_send_message_large.png',
            'opensesame_plugins/titta_send_message/titta_send_message.py',
            'opensesame_plugins/titta_send_message/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/titta_start_recording',
        [
            'opensesame_plugins/titta_start_recording/titta_start_recording.md',
            'opensesame_plugins/titta_start_recording/titta_start_recording.png',
            'opensesame_plugins/titta_start_recording/titta_start_recording_large.png',
            'opensesame_plugins/titta_start_recording/titta_start_recording.py',
            'opensesame_plugins/titta_start_recording/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/titta_stop_recording',
        [
            'opensesame_plugins/titta_stop_recording/titta_stop_recording.md',
            'opensesame_plugins/titta_stop_recording/titta_stop_recording.png',
            'opensesame_plugins/titta_stop_recording/titta_stop_recording_large.png',
            'opensesame_plugins/titta_stop_recording/titta_stop_recording.py',
            'opensesame_plugins/titta_stop_recording/info.yaml',
            ]
        )]
    )
