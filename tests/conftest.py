# MIT License

# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

"""Unit tests fixtures."""

from pathlib import Path
from shutil import copytree, rmtree
from typing import Tuple

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
    project_ = scade.load_project(str(pathname))
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
def tmp_project_session(tmpdir, request) -> Tuple[project.Project, suite.Session]:
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
    pathname = str(target_dir / pathname.name)
    print('loading', pathname)
    project_ = load_project(pathname)
    session = load_session(pathname)
    yield project_, session
    # finalize the test: save both project and model
    # note: the xscade files must have been declared as modified
    print('saving', pathname)
    project_.save(pathname)
    session.save_model2()
