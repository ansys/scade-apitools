.. py:currentmodule:: ansys.scade.apitools

Create SCADE models
===================

Introduction
------------

The SCADE Python API allows modifying SCADE projects and models. This requires a deep knowledge of the underlying meta-model to create consistent instances of classes and associations. Mistakes can lead to corrupted models, difficult to detect, and tool crashes.

The module :py:mod:`create <ansys.scade.apitools.create>` provides higher level functions to ensure the syntactically correctness of the created models.
The overall design consists in having independent functions: it is not required to make several function calls to complete a single modification.

**Important: this library must be used in command line scripts only. Modifying a model from the IDE, while it is loaded, corrupts the internal state of the SCADE Editor and leads to unpredictable results.**

Notes:

* The current version gives only access to the creation of new elements into an existing project or Scade model.

  The edition of a model, for example deleting elements, requires more functions that could be added later on.

* The annotations are not supported yet.
* This library is derived from the existing *SCADE Creation Library* (*SCL*), available for TCL and Python.

  * The functions have been renamed accordingly to PEP8.
  * If most of the interfaces are identical, there are a few changes for providing a more Pythonic way.
  * You can migrate existing applications to use this library, or continue to use *SCL* which is going to be re-implemented on top of this library.

* The functions are all accessible from :py:mod:`create <ansys.scade.apitools.create>`, regardless the submodule they are defined in.

Overall structure of a script
-----------------------------

A script which modifies a Scade model has usually the following architecture:

* Load an existing project: this gives access to two separate sets of data:

  * Project: content of the project file (``.etp``).
  * Scade model: content of the model files (``*.xscade`` and ``*.scade``).

* Add new elements to the project and the model.
* Save the project and the model.

The following script adds a new package to a project::

  """
  Example for creating a package.

  scade.exe -script <project> create_package.py
  """

  from pathlib import Path

  from scade.model.suite import get_roots as get_sessions
  from scade.model.project.stdproject import get_roots as get_projects

  import ansys.scade.apitools.create as create

  def main():
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

When run on an empty project, the new Scade model is as follows:

.. figure:: /create/img/create_package_s.png

The new file is added to the project at the default location:

.. figure:: /create/img/create_package_fv.png

Debugging of a creation script
------------------------------

It is advised to embed the script in an environment which makes first a copy of the model to ease the debugging.

The following script, compatible with any Python IDE, makes a copy of the original model, declares the result project and calls the original script's function main::

  """
  Wrapper of create_package.py for debugging.

  Project: ./Model/Model.etp
  """

  from pathlib import Path
  from shutil import rmtree, copytree

  from ansys.scade.apitools import declare_project

  from create_package import main

  # duplicate the model to a new directory
  dir = Path(__file__).parent
  source_dir = dir / 'Model'
  target_dir = dir / 'Result'
  if target_dir.exists():
      rmtree(target_dir)
  copytree(source_dir, target_dir)

  # declare the duplicated model
  declare_project(str(target_dir / 'Model.etp'))

  # regular script
  main()

Trees
-----

The library does not allow the creation of intermediate elements to prevent the risk of incorrect models because of partial or missing links.
For example, it is not possible to create an instance of ``ExprId`` linked to a constant but not contained by any model element.
Some parts such as types or expressions can be quite large: there are functions to create such trees in an incremental way, which will be compiled when creating the related model element. These intermediate structures, or trees, are used for creating:

* Types
* Expressions
* Transitions
* Control block branches

The next sections introduce the expression and type trees.

Type tree
^^^^^^^^^

A :py:class:`type tree (TT) <create.type.TypeTree>` represents any Scade type. :py:class:`Extended type trees (EX) <create.type.TX>` provide more flexibility by accepting any of the following types:

* :py:class:`Type tree (TT) <create.type.TypeTree>`
* Instance of ``scade.model.suite.Type``
* Name of a predefined type: ``'bool'``, ``'int32'``, ``'float64'``...

There are functions to create complex expression trees, such as structures or arrays, cf. :py:mod:`create.type <ansys.scade.apitools.create.type>`.

The following example adds a simple type to a model::

    # add a new type to the model, in the default file for root declarations
    speed = create.create_named_type(model, 'Speed', 'float32', path=None)

The next example creates an array of points::

    # add an array of points
    tree = create.create_structure(('x', 'float32'), ('y', 'float32'))
    point = create.create_named_type(model, 'Point', tree)
    tree = create.create_table(9, point)
    polyline = create.create_named_type(model, 'polyline', tree)

Although this is not advised, it is possible to combine type trees::

    # add an array of anonymous (x, y)
    tree_struct = create.create_structure(('x', 'float32'), ('y', 'float32'))
    tree_table = create.create_table(9, tree_struct)
    polyline2 = create.create_named_type(model, 'polyline2', tree_table)

Refer to the module :py:mod:`create.type <ansys.scade.apitools.create.type>` for a complete reference and the functions to create any type tree.

..
  :py:func:`create.declaration.create_named_type`

Expression tree
^^^^^^^^^^^^^^^

An :py:class:`expression tree (ET) <create.expression.ExpressionTree>` represents any Scade expression, made of operators and operands. :py:class:`Extended expression trees (EX) <create.expression.EX>` provide more flexibility by accepting any of the following types:

* :py:class:`Expression tree (ET) <create.expression.ExpressionTree>`
* Instance of ``scade.model.suite.ConstVar``
* Scade literals: ``'true'``, ``'3.14_f32'``
* Python literals: ``True``, ``42``, ``3.14``, ``'c'``...

The following example adds two constants to a model. The first one, ``N`` is an integer and its expression is the literal ``42``. The second one, ``N2``, requires an expression tree to specify its value::

    # constant N: int32 = 42
    cst_n = create.create_constant(model, 'N', 'int32', 42)
    # constant N2: int32 = N * N
    tree = create.create_nary('*', cst_n, cst_n)
    cst_n2 = create.create_constant(model, 'N2', 'int32', tree)

Refer to the module :py:mod:`create.expression <ansys.scade.apitools.create.expression>` for a complete reference and the functions to create any expression tree.
