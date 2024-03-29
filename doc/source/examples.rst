Examples
========

This section provides examples organized by Scade models. These models are not
necessarily correct. They simply provide some data for the scripts to process.

The overall structure of an example script is as follows:

* Retrieve one or more Scade model elements from the project.
* Apply a command from ``ansys.scade.apitools`` to these elements.
* Print some feedback.

.. note::
    The examples for the :py:mod:`create <ansys.scade.apitools.create>`
    package have a different design, described in the appropriate example sections.

Run the examples
----------------

For a reminder on SCADE Python scripts, see :ref:`SCADE scripting <scripting scade>`.

SCADE GUI
~~~~~~~~~
The examples associated with a Scade model are referenced in the project:

* Load the model with the SCADE Suite.
* From the **FileView**, open any script.
* To execute the script, select **Tools > Execute script**.
* In the **Output** window, observe the result on the **Script** tab.

SCADE CLI
~~~~~~~~~
The easiest way to use the SCADE CLI consists of setting the current directory to the
considered example's directory and running the ``scade.exe -script`` command:

.. code:: bash

    scade.exe -script <project> <script>

Python
~~~~~~

You must declare the model to use to run the example prior to executing the script.

#. Change the current directory to the considered example's directory. For example, ``examples/query_type``.

   .. code:: bash

       > cd examples\query_type

#. Run a Python 3.7 or 3.10 session, depending on the SCADE release installed on your computer.

   .. code:: bash

       > where python.exe
       C:\Users\jhenry\AppData\Local\Programs\Python\Python310\python.exe
       > python.exe

#. Declare the project.

   .. code:: python

       >>> from ansys.scade.apitools import declare_project
       >>> declare_project('QueryType.etp')

#. Copy/paste the content of a script or run it as follows:

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
