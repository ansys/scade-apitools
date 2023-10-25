.. _scripting scade:

SCADE scripting
===============

Reminder
--------

Most of the SCADE Python APIs available in the SCADE IDE are proxies to internal C++ or Java kernels.
The most popular are the following ones:

* SCADE Suite
* SCADE Test
* SCADE Architect

Refer to the section *API Capabilities by SCADE Products* of the SCADE documentation for details.

This provides advantages that won't be discussed here, but it has also a few constraints:

* The scripts can't be run outside of the context of a SCADE Release, on Windows.
* The version of the Python interpreter must be the one delivered with SCADE Suite:

  * Python 3.7 for releases prior to 2023 R2 (directory SCADE/contrib/Python37)
  * Python 3.10 starting from 2023 R2 (directory SCADE/contrib/Python310)

SCADE environment
-----------------

The SCADE Python scripts, and formerly TCL scripts, are intended to be run from a SCADE environment, either the SCADE IDE or the command line through ``scade.exe -script``.

The operating mode is identical in both cases. When a script is run:

* The projects are already loaded: Workspace in the IDE or list on the command line.
  There is no command to load dynamically a project and its related semantic data, for example SCADE Suite models or SCADE Test procedures.

* SCADE creates the instance of a Python interpreter and adds dynamically commands to address the loaded data, through the module ``scade``.
  As mentioned above, it is not possible to use another interpreter as the one delivered in SCADE/contrib, or to specify a virtual environment based on it.

  There are additional functions in the IDE to address features for queries or reporting, for example ``scade.selection`` or ``scade.report``.

* The interpreter is deleted once the execution of the scripts ends.

There is another advanced kind of scripts in the IDE: SCADE custom extensions.
These scripts are run at startup or when a workspace is loaded, and live until the application ends or the project is closed.
The Python interpreters have more functions to extend the user interface with GUI artifacts such as toolbars, menus or property pages.

Python environment
------------------

The usage described in the previous section has been used for a couple of decades for TCL scripts, and more recently, Python scripts.
Python allows developing much more complex components and benefits from powerful IDEs such as PyCharm, VS Code or PTVS.
Although it is not possible to develop GUI scripts in Python IDEs, SCADE provides some workarounds to the constraints exposed in the previous section for command line scripts,
to allow the usage of these IDEs.

In addition to the directories to be added to ``PYTHONPATH``, there is a module ``scade_env`` which **must** be imported before accessing any SCADE Python modules.
This module emulates the context of ``scade.exe -script``, and allows declaring all the projects to load before using the SCADE APIs.

*Note*: The import of this module and the declaration of projects are ignored when the script is run in a SCADE environment.

Refer to the section *Executing Scripts in Python Environment* of the SCADE documentation for details.

Advanced usage with API Tools
-----------------------------

Once the constraints of the SCADE Python APIs and their usage in a Python environment are understood,
it is possible to simplify and extend the domain of usage of the scripts, in batch mode.

The module ``ansys.scade.apitools`` imports ``scade_env`` and exposes its function ``load_project``, renamed to ``declare_project`` to avoid ambiguities.
Setting ``PYTHONPATH`` as specified in the documentation becomes optional.
When ``PYTHONPATH`` does not refer to a SCADE environment, ``apitools`` has several strategies to find and add dynamically the required SCADE directories to ``sys.path``,
depending on ``sys.executable``:

* Interpreter delivered in ``SCADE/contrib/PythonXxx``: The directories are relative to its location.
* Interpreter of a virtual environment on top of an interpreter delivered with SCADE: The virtual environment is resolved, then same as above.
* Independent interpreter: ``apitools`` selects the most recent version of SCADE installed on the computer which is compatible with the current interpreter, then same as above:

  * Python 3.7: from 2021 R1 to 2023 R1.
  * Python 3.10: from 2023 R2.

If none of the above uses cases applies, the script cannot be executed.

Example of interactive session with a standard installation of Python:

1. Interactive session

.. code:: python

    > where python.exe
    C:\Users\jhenry\AppData\Local\Programs\Python\Python310\python.exe
    > python.exe
    Python 3.10.10 (tags/v3.10.10:aad5f6a, Feb  7 2023, 17:20:36) [MSC v.1929 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.

2. Preamble to activate a SCADE environment on a given project

.. code:: python

    >>> from ansys.scade.apitools import declare_project
    >>> declare_project(r'C:\Program Files\ANSYS Inc\v232\SCADE\examples\ABC_N\ABC_N.etp')

3. Regular script: Load the declared projects and access their pathname

.. code:: python

    >>> from scade.model.project.stdproject import get_roots as get_projects
    >>> for project in get_projects():
    ...     print(project.pathname)
    ...
    C:/Program Files/ANSYS Inc/v232/SCADE/examples/ABC_N/ABC_N.etp
