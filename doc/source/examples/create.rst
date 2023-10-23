create
======

These complete examples illustrate the usage of the creation functions.

They provide hints about the setup of a test environment and correspond to frequent requests.

These examples illustrate the usage of the intermediate structures introduced to create
complex types and expressions, as well as the creation of control blocks.

It might be a good idea to run the examples step by step with a debugger to get
a better understanding of the code.

Test environment
----------------

The examples modify a project. Each example comes with a wrapper script which runs the example
on a copy of the input model.

The wrapper scripts, named ``debug_<name of the script>.py``, are  designed to be used in
a Python IDE, with the following pattern::

    from pathlib import Path
    from shutil import copytree, rmtree

    from ansys.scade.apitools import declare_project

    # isort: split

    import create_xxx

    # duplicate the model to a new directory
    dir = Path(__file__).parent
    source_dir = dir / 'Template'
    target_dir = dir / 'Result'
    if target_dir.exists():
        rmtree(target_dir)
    copytree(source_dir, target_dir)

    # declare the duplicated model
    declare_project(str(target_dir / 'Model.etp'))

    # regular script
    create_xxx.main()

Examples
--------

.. toctree::
   :maxdepth: 1

   create_if_block
   create_interface.rst
   create_make.rst
   create_state_machine.rst
   create_top_level.rst
   create_when_block.rst
