"""
Example for creating operator interfaces.

The description file is hard-coded to interface.txt, in the script's directory.

Its syntax is very simple: each line declares an operator,
an input or an output, as shown in the following example::

    N op1
    I i1 int
    I i2 int
    O o1 real


Usage::

    scade.exe -script <project> create_interface.py

"""

from pathlib import Path

import scade.model.project.stdproject as std
import scade.model.suite as suite

import ansys.scade.apitools.create as create

# global cache for the predefined and existing types
types = {}


def cache_types(session: suite.Session):
    """
    Cache all the types of a Scade model and its libraries into a dictionary, by path.

    Parameters
    ----------
        session : suite.Session
            Entry point for the loaded model.

    """
    global types

    # consider the model and its libraries
    types = {_.get_full_path().strip('/'): _ for _ in session.model.all_named_types}

    # add the predefined types
    names = [
        'bool',
        'char' 'int8',
        'int16',
        'int32',
        'int64',
        'uint8',
        'uint16',
        'uint32',
        'uint64',
        'float32',
        'float64',
    ]
    types.update({_: session.find_predefined_type(_) for _ in names})


def add_operator(project: std.Project, model: suite.Model, name: str) -> suite.Operator:
    """
    Add a new operator to the model, and add its separate storage file in the project.

    Parameters
    ----------
        project : std.Project
            Input project.

        model : suite.Model
            Input model.

        name : str
            Name of the operator.

    Returns
    -------
        suite.Operator
    """
    # store the operator in the project's directory
    path = Path(project.pathname).with_name(name + '.xscade')
    # create the operator in the model, assuming it is a node
    operator = create.create_graphical_operator(model, name, path, state=True)
    # add the separate file to the project
    create.add_element_to_project(project, operator)
    return operator


def create_interface(project: std.Project, model: suite.Model, description: Path):
    """
    Read the description file and create the operators and their I/Os.

    Parameters
    ----------
        project : std.Project
            Input project.

        model : suite.Model
            Input model.

        description : Path
            Text file describing the operators to create.
    """
    # for line in description.read().split('\n'):
    for line in description.open():
        line = line.strip('\n ')
        if line == '' or line[0] == '#':
            continue
        tokens = line.split()
        if len(tokens) == 2 and tokens[0] == 'N':
            operator = add_operator(project, model, tokens[1])
        elif len(tokens) == 3 and tokens[0] == 'I':
            name, type_ = tokens[1:]
            create.add_operator_inputs(operator, [(name, types[type_])], None)
        elif len(tokens) == 3 and tokens[0] == 'O':
            name, type_ = tokens[1:]
            create.add_operator_outputs(operator, [(name, types[type_])], None)
        else:
            # syntax error
            print('%s: Syntax error' % line)

    create.save_project(project)
    create.save_all()


def main(description: Path = None):
    """
    Create the operators and their interface into the model.

    Parameters
    ----------
        description : Path
            Optional input description file.

            When not specified, the parameter is set to 'interface.txt',
            expected to be in the script's directory.

    """
    # load the SCADE project and model
    # note: the script shall be launched with a single projet
    project = std.get_roots()[0]
    session = suite.get_roots()[0]
    # the description file is in the same directory
    description = Path(__file__).with_name('interface.txt')
    # cache all the types of the model and its libraries
    cache_types(session)
    # create the interface from the description file
    create_interface(project, session.model, description)


if __name__ == "__main__":
    # launched from scade -script
    main()
