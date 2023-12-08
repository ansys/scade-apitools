# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

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

# shall modify sys.path to access SCADE APIs
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
def test_get_compatible_scade_home(tc):
    # make sure at least one SCADE version is available for one of 3.4, 3.7, 3.10
    # and not available for a few other versions
    versions, status = tc
    homes = []
    for version in versions:
        home = apitools.auto_scade_env.get_compatible_scade_home(version)
        if home:
            homes.append(home)
    assert (len(homes) != 0) == status
