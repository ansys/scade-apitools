# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
