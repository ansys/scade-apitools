# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
