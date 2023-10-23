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

"""
Provide load_project from scade_env.

Search for a scade installation compatible with the Python version
and add it to sys.path if not already present.
Present means scade_env.pyd is accessible from sys.path.
"""

import importlib
from pathlib import Path
import platform
import re
import sys

if platform.system() == 'Windows':
    import winreg as reg
else:
    # allow importing the file on other systems
    pass


def resolve_venv(home: Path) -> Path:
    """Return the virtual environment's target, if any."""
    cfg = home / 'pyvenv.cfg'
    if cfg.exists():
        for line in cfg.open('r'):
            m = re.match('^home\s*=\s*(.*)$', line)
            if m:
                return Path(m.groups()[0]).parent
    return None


def get_scade_dirs(min='00.0', max='99.9'):
    """Return the list of SCADE installation directories."""
    names = []
    if platform.system() == 'Windows':
        for company in 'Esterel Technologies', 'Ansys Inc':
            hklm = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, 'SOFTWARE\%s\SCADE' % company)
            for i in range(reg.QueryInfoKey(hklm)[0]):
                name = reg.EnumKey(hklm, i)
                try:
                    dir, _ = reg.QueryValueEx(reg.OpenKey(hklm, name), 'InstallDir')
                    names.append((name, dir))
                except FileNotFoundError:
                    pass
    dirs = []
    for name, dir in sorted(names, key=lambda x: x[0]):
        if name >= min and name < max:
            dirs.append(dir)
            # print('short list', dir)
    return dirs


def get_python_scade_versions(python_version: str):
    """Return the highest SCADE installation compatible with a version of Python."""
    # [min, max[ releases for a given version of Python
    releases = {
        '3.4': ('19.2', '21.2'),
        '3.7': ('21.2', '23.2'),
        '3.10': ('23.2', '99.9'),
    }
    interval = releases.get(python_version)
    return interval


def get_compatible_scade_home(version: str) -> Path:
    """Return the most recent version of SCADE compatible with the input Python version."""
    interval = get_python_scade_versions(version)
    if interval:
        dirs = get_scade_dirs(*interval)
        if dirs:
            # ordered list, get the most recent compatible version
            # and leave a message for who might read it
            # print('Using', dirs[-1])
            return Path(dirs[-1])
    return None


def add_scade_to_sys_path():
    """Add to sys.path an installed SCADE release compatible with the current interpreter."""
    # resolve virtual environments to get SCADE's Python interpreter
    home = Path(sys.executable).parent.parent
    _wrapped_home = resolve_venv(home)
    while _wrapped_home:
        home = _wrapped_home
        _wrapped_home = resolve_venv(home)

    if home.name == 'contrib':
        # python.exe is located in <SCADE install>/contrib/Python3x
        home = home.parent
    else:
        # last chance, try the most recent installation of SCADE
        major, minor, _, _, _ = sys.version_info
        version = '%d.%d' % (major, minor)
        home = get_compatible_scade_home(version)

    if not home:  # pragma no cover
        # wrong installation or SCADE not available on the computer
        print('Use a Python interpreter delivered with SCADE.')
    else:
        # regular SCADE installation
        _base = home / 'SCADE'
        sys.path.append(str(_base / 'bin'))
        sys.path.append(str(_base / 'APIs' / 'Python' / 'lib'))


if platform.system() == 'Windows':
    # scade_env.pyd is in <scade installation>/SCADE/bin
    if not importlib.util.find_spec("scade_env"):
        add_scade_to_sys_path()

    # ignore F401: declare_project made available for modules, not used here
    # import also _scade_api and scade, to avoid import order constraint in client files

    from scade_env import load_project as declare_project  # noqa: F401

    # some fake statement to prevent isort to change the order of the next import directives
    _ = 0
    import _scade_api  # noqa: F401
    import scade  # noqa: F401
else:
    # allow importing the file on other systems
    # for documentation generation, for example
    declare_project = None
    scade = None
    _scade_api = None
