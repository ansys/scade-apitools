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

"""Access to SCADE installation info."""

import inspect
from pathlib import Path
import platform
from typing import Dict

if platform.system() == 'Windows':
    import scade_env
else:
    # allow importing the file on other systems
    # for documentation generation, for example
    pass


def get_scade_home() -> Path:
    """
    Return the SCADE installation directory.

    For example: C:/Program Files/ANSYS Inc/v232/SCADE
    """
    # we can't rely on the usual variables SCADE and ETBIN which are not set
    # when the script is run through python.exe instead od scade.exe -script.
    # we derive the scade home directory from the location of the module scade_env
    # which is locate in <home>/SCADE/bin
    scade_home = Path(inspect.getfile(scade_env))
    return scade_home.parent.parent.parent


def get_scade_properties() -> Dict[str, str]:
    """Return the content of <home>/common/scade.properties as a dictionary."""
    scade_home = get_scade_home()
    # the file must exist for any release of SCADE using Python 3.7, at least until 2023 R2
    with (scade_home / 'common' / 'scade.properties').open() as f:
        tokens = [_.split('=', 1) for _ in f.read().split('\n') if _]
        d = {_[0]: _[1] for _ in tokens}
    return d


def get_scade_version() -> int:
    """Return the version of SCADE, for example 232 for 2023 R2."""
    props = get_scade_properties()
    return int(props['SCADE_STUDIO_NUMBER'][:3])