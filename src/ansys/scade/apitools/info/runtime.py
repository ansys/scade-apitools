# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.
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

"""Access to SCADE runtime info."""

import builtins
import sys

import scade

ide = 'activate' in dir(scade)
"""Indicate whether the script runs with the SCADE Studio environment."""


def ide_print(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    """Alternative to print based on scade.output."""
    if file == sys.stdout or file == sys.stderr:
        if sep is None:
            sep = ' '
        if end is None:
            end = '\n'
        text = sep.join([str(_) for _ in args])
        scade.output(text + end)
    else:
        builtins.print(*args, sep, end, file, flush)


print = ide_print if ide else builtins.print
"""Emulation of print for SCADE Studio environment."""
