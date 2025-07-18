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

"""Unit tests fixtures."""

from pathlib import Path
from shutil import copytree, rmtree
from typing import Any, Generator, Tuple

import pytest

# shall modify sys.path to access SCACE APIs
from ansys.scade.apitools import scade

# must be imported after apitools
# isort: split
import scade.model.project.stdproject as project
import scade.model.suite as suite


def pytest_configure(config):
    """Declare the markers used in this project."""
    config.addinivalue_line('markers', 'project: project to be loaded')


@pytest.fixture(scope='session')
def tmpdir():
    """Create/empty the temporary directory for output files."""
    path = Path('tests') / 'tmp'
    try:
        rmtree(str(path))
    except FileNotFoundError:
        pass
    path.mkdir()
    return path


def load_session(pathname: Path) -> suite.Session:
    """
    Load a Scade model in a separate environment.

    Note: The model can have unresolved references since the libraries
    are not loaded.
    """
    session = suite.Session()
    session.load2(str(pathname))
    assert session.model
    return session


def load_project(pathname: Path) -> project.Project:
    """
    Load a Scade project in a separate environment.

    Note: Undocumented API.
    """
    # scade is a CPython module defined dynamically
    project_ = scade.load_project(str(pathname))  # type: ignore
    return project_


@pytest.fixture(scope='function')
def project_session(request) -> Tuple[project.Project, suite.Session]:
    """
    Load a project and the corresponding Scade model.

    Specify the project to load with the marker ``project``.
    """
    marker = request.node.get_closest_marker('project')
    # marker is None if the test is not designed correctly
    assert marker
    pathname = marker.args[0]
    project_ = load_project(pathname)
    session = load_session(pathname)
    return project_, session


@pytest.fixture(scope='class')
def tmp_project_session(
    tmpdir, request
) -> Generator[Tuple[project.Project, suite.Session], Any, Any]:
    """
    Load a temporary copy of the project, and save it once the test is terminated.

    This fixture shall be associated to a class, and the temporary directory is
    ``tmpdir/<class name>``.

    Specify the project to load with the marker ``project``.
    """
    marker = request.node.get_closest_marker('project')
    # marker is None if the test is not designed correctly
    assert marker
    pathname = marker.args[0]
    # duplicate the project to edit it safely
    target_dir = tmpdir / request.cls.__name__
    copytree(pathname.parent, target_dir)
    path = target_dir / pathname.name
    print('loading', path)
    project_ = load_project(path)
    session = load_session(path)
    yield project_, session
    # finalize the test: save both project and model
    # note: the xscade files must have been declared as modified
    print('saving', path)
    project_.save(str(path))
    session.save_model2()
