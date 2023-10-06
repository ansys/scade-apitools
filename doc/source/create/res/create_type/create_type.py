"""
Example for creating types.

scade.exe -script <project> create_type.py
"""

from scade.model.project.stdproject import get_roots as get_projects
from scade.model.suite import get_roots as get_sessions

import ansys.scade.apitools.create as create


def main():
    """Entry point."""
    project = get_projects()[0]
    model = get_sessions()[0].model

    # add a new type to the model, in the default file for root declarations
    speed = create.create_named_type(model, 'Speed', 'float32', path=None)

    # add an array of points
    tree = create.create_structure(('x', 'float32'), ('y', 'float32'))
    point = create.create_named_type(model, 'Point', tree)
    tree = create.create_table(9, point)
    polyline = create.create_named_type(model, 'polyline', tree)

    # add an array of anonymous (x, y)
    tree_struct = create.create_structure(('x', 'float32'), ('y', 'float32'))
    tree_table = create.create_table(9, tree_struct)
    polyline2 = create.create_named_type(model, 'polyline2', tree_table)

    create.save_all()

    # add the file associated to one of the types to the project
    create.add_element_to_project(project, speed)
    # save the project file
    create.save_project(project)


if __name__ == '__main__':
    main()
