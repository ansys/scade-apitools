Examples
========

Overview
--------
The examples are organized by SCADE models. These models are not necessarily correct, they intend to provide some data to be processed by the scripts.

The overall structure of an example script is as follows:

* Retrieve one or more Scade model elements from the project.
* Apply a command from ``ansys.scade.apitools`` to these elements.
* Print some feedback.

Run the examples
----------------

Refer to :ref:`SCADE scripting <scripting scade>` for a reminder on SCADE Python scripts.

SCADE GUI
~~~~~~~~~
The examples associated to a Scade model are referenced in the project:

* Load the model with the SCADE Suite.
* Open any script from the `FileView`.
* Execute the script with the command `Tools/Execute script`.
* Observe the result in the tab `Script` from the window `Output`.

SCADE CLI
~~~~~~~~~

The easiest way consists in setting the current directory to the considered example's directory and run ``scade.exe -script``::

    scade.exe -script <project> <script> 

Python
~~~~~~

The model used to run the example must be declared prior to the script execution.

* Change the current directory to the considered example's directory, for example `examples/query_type` ::

    > cd examples\query_type

* Run a Python 3.7 or 3.10 session depending on the release of SCADE  installed on your computer ::

    > where python.exe
    C:\Users\jhenry\AppData\Local\Programs\Python\Python310\python.exe
    > python.exe

* Declare the project

    >>> from ansys.scade.apitools import declare_project
    >>> declare_project('QueryType.etp')

* Copy/paste the content of a script or run it as follows ::

    >>> exec(open('get_type_name.py').read())

Examples
--------

.. toctree::

   _examples/expr_access 
   _examples/info 
   _examples/prop_pragma 
   _examples/query_type 

..
    .. include:: _examples/query_type.rst
