"""
Example for creating constants.

scade.exe -script <project> create_constant.py
"""

from scade.model.project.stdproject import get_roots as get_projects
from scade.model.suite import get_roots as get_sessions

import ansys.scade.apitools.create as create


def main():
    """Entry point."""
    project = get_projects()[0]
    model = get_sessions()[0].model

    # constant N: int32 = 42
    cst_n = create.create_constant(model, 'N', 'int32', 42)
    # constant N2: int32 = N * N
    tree = create.create_nary('*', cst_n, cst_n)
    cst_n2 = create.create_constant(model, 'N2', 'int32', tree)
    # save the Scade model
    create.save_all()

    # add one of the ocnstants to the project file
    create.add_element_to_project(project, cst_n)
    # save the project file
    create.save_project(project)


if __name__ == '__main__':
    main()
