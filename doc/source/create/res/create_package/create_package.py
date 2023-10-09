"""
Example for creating a package.

scade.exe -script <project> create_package.py
"""

from pathlib import Path

from scade.model.project.stdproject import get_roots as get_projects
from scade.model.suite import get_roots as get_sessions

import ansys.scade.apitools.create as create


def main():
    """Entry point."""
    project = get_projects()[0]
    session = get_sessions()[0]

    # create a new package in the project's directory
    path = Path(project.pathname).parent / 'MyPackage.xscade'
    package = create.create_package(session.model, 'MyPackage', path)
    # save the Scade model
    create.save_all()

    # add the package to the project file
    create.add_element_to_project(project, package)
    # save the project file
    create.save_project(project)


if __name__ == '__main__':
    main()
