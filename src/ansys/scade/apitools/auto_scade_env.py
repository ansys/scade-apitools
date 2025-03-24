# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
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
Provides ``scade_env.load_project``, renamed to ``declare_project``.

Search for a SCADE installation compatible with the Python version
and add it to ``sys.path`` if not already present.
Present means ``scade_env.pyd`` is accessible from ``sys.path``.
"""

import importlib.util
from pathlib import Path
import platform
import re
import sys
from typing import Optional

if platform.system() == 'Windows':
    import winreg as reg
else:
    # allow importing the file on other systems
    pass


def _resolve_venv(home: Path) -> Optional[Path]:
    """Get the virtual environment's target, if any."""
    cfg = home / 'pyvenv.cfg'
    if cfg.exists():
        for line in cfg.open('r'):
            m = re.match(r'^home\s*=\s*(.*)$', line)
            if m:
                return Path(m.groups()[0]).parent
    return None


def _get_scade_dirs(min='00.0', max='99.9'):
    """Get the list of SCADE installation directories."""
    names = []
    if platform.system() == 'Windows':
        for company in 'Esterel Technologies', 'Ansys Inc':
            try:
                hklm = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\%s\SCADE' % company)
            except OSError:
                continue
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


def _get_python_scade_versions(major: int, minor: int):
    """Get the highest SCADE installation compatible with a version of Python."""
    # [min, max[ releases for a given version of Python
    releases = {
        4: ('19.2', '21.2'),
        7: ('21.2', '23.2'),
        10: ('23.2', '26.1'),
        12: ('26.1', '99.9'),
    }
    if major != 3:
        return None
    if minor > 12:
        # starting 3.12, SCADE uses the Python Limited API
        minor = 12
    interval = releases.get(minor)
    return interval


def _get_compatible_scade_home(major: int, minor: int) -> Optional[Path]:
    """Get the most recent version of SCADE compatible with the input Python version."""
    interval = _get_python_scade_versions(major, minor)
    if interval:
        dirs = _get_scade_dirs(*interval)
        if dirs:
            # ordered list, get the most recent compatible version
            # and leave a message for who might read it
            # print('Using', dirs[-1])
            return Path(dirs[-1])
    return None


def _add_scade_to_sys_path():
    """Add to ``sys.path`` an installed SCADE release compatible with the current interpreter."""
    # resolve virtual environments to get SCADE's Python interpreter
    home = Path(sys.executable).parent.parent
    _wrapped_home = _resolve_venv(home)
    while _wrapped_home:
        home = _wrapped_home
        _wrapped_home = _resolve_venv(home)

    if home.name == 'contrib':
        # python.exe is located in <SCADE install>/contrib/Python3x
        home = home.parent
    else:
        # last chance, try the most recent installation of SCADE
        major, minor, _, _, _ = sys.version_info
        home = _get_compatible_scade_home(major, minor)

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
        _add_scade_to_sys_path()

    from scade_env import load_project as declare_project

    # import also _scade_api and scade, to avoid import order constraint in client files
    # isort: split
    import _scade_api
    import scade
else:
    # allow importing the file on other systems
    # for documentation generation, for example
    declare_project = None
    scade = None
    _scade_api = None
