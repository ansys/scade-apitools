# MIT License
#
# Copyright (c) 2023 ANSYS, Inc. All rights reserved.
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
Test suite for auto_scade_env.py.

It is not possible to test exhaustively the module, since it depends on
the way the Python environment is setup and on the various SCADE
installations available on the computer.

Test strategy:
* Make sure we can import SCADE modules.
* Make sure the individual functions return some value and don't raise
  any exception.
"""

import pytest

# shall modify sys.path to access SCACE APIs
import ansys.scade.apitools as apitools


def test_auto_scade_env():
    # shall be able to import scade.model.project.stdproject
    import scade.model.project.stdproject as std

    assert std.get_roots


@pytest.mark.parametrize(
    'tc',
    [
        (['2.7', '3.8'], False),
        (['3.4', '3.7', '3.10'], True),
    ],
)
def test_get_scade_home(tc):
    # make sure at least one SCADE version is available for one of 3.4, 3.7, 3.10
    # and not available for a few other versions
    versions, status = tc
    homes = []
    for version in versions:
        home = apitools.auto_scade_env.get_scade_home(version)
        if home:
            homes.append(home)
    assert (len(homes) != 0) == status
