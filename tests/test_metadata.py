# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.

from ansys.scade.apitools import __version__


def test_pkg_version():
    assert __version__ == "0.1.dev0"
