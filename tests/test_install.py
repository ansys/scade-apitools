# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

"""
Test suite for install.py.

Test strategy:

The test can be run with different releases of SCADE: The values can't be compared
to predefined ones.
The tests make sure the functions execute properly and return consistent data.
"""

from pathlib import Path
import sys

import ansys.scade.apitools.info as info
import ansys.scade.apitools.info.install as install


def test_get_scade_home():
    home = info.get_scade_home()
    # home must not be None and must contain 'SCADE'
    assert Path(home / 'SCADE').exists()


def test_get_scade_properties():
    props = install.get_scade_properties()
    # make sure some properties exist
    assert props['INSTALL_FOLDER']


def test_get_scade_version():
    version = info.get_scade_version()
    # 3 digits
    assert version > 100 and version < 999
    # check the consistency of the value is consistent, for example by
    # the version of the interpreter
    _, minor, _, _, _ = sys.version_info
    if minor == 7:
        assert version < 232
    else:
        assert version >= 232
