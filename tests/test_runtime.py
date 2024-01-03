# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

"""
Test suite for runtime.py.

Test strategy:

The test can be run only in batche mode.
The tests make sure the functions execute properly and return consistent data.
"""

import builtins

import ansys.scade.apitools.info as info
import ansys.scade.apitools.info.runtime as runtime


def test_ide():
    # tests run in batch mode
    assert not info.ide


def test_print():
    # tests run in batch mode
    assert runtime.print == builtins.print


def test_ide_print(capsys):
    # print some text with ide_print and print and compare the results
    args = ['abc', 'd\ne', 'f g']
    # ignore prior outputs if any
    _ = capsys.readouterr()
    # standard print
    print(*args, sep='-', end='.\n')
    builtin_result = capsys.readouterr().out
    _ = capsys.readouterr().out
    # ide_print
    runtime.ide_print(*args, sep='-', end='.\n')
    ide_result = capsys.readouterr().out
    assert ide_result
    # scade.output does not behave as expected in pytest environment
    # --> not testable
    # assert builtin_result == ide_result
    assert builtin_result
