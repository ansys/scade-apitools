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

"""Helpers for test_*.py."""

import difflib
from inspect import getsourcefile
import os
from pathlib import Path


def get_resources_dir() -> Path:
    """Return the directory ./resources relative to this file's directory."""
    script_path = Path(os.path.abspath(getsourcefile(lambda: 0)))
    return script_path.parent


def cmp_log(log_file, lines) -> bool:
    """Return True if the file is identical to a list of strings."""
    l = list(open(log_file))
    l = [line.strip('\n') for line in l]
    return l == lines


def cmp_file(fromfile: str, tofile: str, n=3, linejunk=None):
    """Return the differences between two files."""
    with open(fromfile) as fromf, open(tofile) as tof:
        if linejunk:
            fromlines = [line for line in fromf if not linejunk(line)]
            tolines = [line for line in tof if not linejunk(line)]
        else:
            fromlines, tolines = list(fromf), list(tof)

    diff = difflib.context_diff(fromlines, tolines, fromfile, tofile, n=n)
    return diff
