# MIT License

# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

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
    log_lines = list(open(log_file))
    log_lines = [line.strip('\n') for line in log_lines]
    return log_lines == lines


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
