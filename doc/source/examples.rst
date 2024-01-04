Examples
========

This section provides examples that are organized by Scade models. These models are not
necessarily correct. They simply provide some data to be processed by the scripts.

The overall structure of an example script is as follows:

* Retrieve one or more Scade model elements from the project.
* Apply a command from ``ansys.scade.apitools`` to these elements.
* Print some feedback.

.. note::
    The examples for the :py:mod:`create <ansys.scade.apitools.create>`
    module have a different design, described in the appropriate section.

Run the examples
----------------

For a reminder on SCADE Python scripts, see :ref:`SCADE scripting <scripting scade>` .

SCADE GUI
~~~~~~~~~
The examples associated with a Scade model are referenced in the project:

* Load the model with the SCADE Suite.
* From the **FileView**, open any script.
* To execute the script, run the ``Tools/Execute script`` command.
* In the **Output** window, observe the result in **Script** tab.

SCADE CLI
~~~~~~~~~
The easiest way consists in setting the current directory to the considered example's directory and
run the ``scade.exe -script`` command:

.. code:: bash

    scade.exe -script <project> <script>

Python
~~~~~~

The model used to run the example must be declared prior to the script execution.

* Change the current directory to the considered example's directory. For example, ``examples/query_type``.

.. code:: bash

    > cd examples\query_type

* Run a Python 3.7 or 3.10 session depending on the release of SCADE installed on your computer.

.. code:: bash

    > where python.exe
    C:\Users\jhenry\AppData\Local\Programs\Python\Python310\python.exe
    > python.exe

* Declare the project.

.. code:: python

    >>> from ansys.scade.apitools import declare_project
    >>> declare_project('QueryType.etp')

* Copy/paste the content of a script or run it as follows:

.. code:: python

    >>> exec(open('get_type_name.py').read())

Examples
--------

.. toctree::
   :maxdepth: 1

   examples/create
   _examples/expr_access
   _examples/info
   _examples/prop_pragma
   _examples/query_type

..
    .. include:: _examples/query_type.rst
