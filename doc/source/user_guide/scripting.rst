.. _scripting scade:

SCADE scripting
===============

Reminder
--------

Most of the SCADE Python APIs available in the SCADE IDE are proxies to internal C++ or Java kernels.
These are the most popular ones:

* SCADE Suite
* SCADE Test
* SCADE Architect

For more information, see *API Capabilities by SCADE Products* in the SCADE documentation.

This provides advantages that won't be discussed here. However, it also has a few constraints:

* The scripts can't be run outside of the context of a SCADE release on Windows.
* The version of the Python interpreter must be the one delivered with the SCADE Suite:

  * Python 3.7 for releases prior to 2023 R2 (The directory is ``SCADE/contrib/Python37``.)
  * Python 3.10 starting from 2023 R2 (The directory is ``SCADE/contrib/Python310``.)

SCADE environment
-----------------

The SCADE Python scripts, and formerly TCL scripts, are intended to be run from a SCADE
environment, either in the SCADE IDE or from the command line using the ``scade.exe -script``
command.

The operating mode when running a script is identical in both environments.

* The projects are already loaded, either in the workspace in the IDE or from a list
  on the command line. There is no command to dynamically load a project and its related
  semantic data, such as SCADE Suite models or SCADE Test procedures.

* SCADE creates an instance of a Python interpreter and dynamically adds commands to address
  the loaded data through the ``scade`` module. As mentioned in the preceding bullet, it is
  not possible to use an interpreter other than the one delivered in the ``SCADE/contrib``
  directory or to specify a virtual environment based on it.

  The IDE provides additional features for queries and reporting,
  including the ``scade.selection`` and ``scade.report`` functions.

* The interpreter is deleted once the execution of the scripts ends.

SCADE custom extensions are another advanced kind of scripts in the IDE. These scripts
are run at startup or when a workspace is loaded. They live until the app ends or
the project is closed. Python interpreters have more functions to extend the user interface
with GUI artifacts such as toolbars, menus, and property pages.

Python environment
------------------

The behaviors described in the previous section have been used for a couple of decades
for TCL scripts, and more recently, Python scripts. Python allows developing much more
complex components and benefits from powerful IDEs such as PyCharm, Visual Studio Code,
and PTVS (Python Tools for Visual Studio). Although it is not possible to develop GUI
scripts in Python IDEs, SCADE provides some workarounds to the preceding constraints
for command line scripts to allow for using these IDEs.

In addition to the directories to be added to the ``PYTHONPATH`` environment variable,
there is a ``scade_env`` module that must be imported before accessing any SCADE Python
module. The ``scade_env`` module emulates the context of the ``scade.exe -script`` command.
It allows you to declare all the projects to load before using the SCADE APIs.

.. note::
   The import of the ``scade_env`` module and the declaration of projects are ignored when
   the script is run in a SCADE environment.

For more information, see *Executing Scripts in Python Environment* in the SCADE documentation.

Advanced usage with API tools
-----------------------------

Once the constraints of the SCADE Python APIs and their usage in a Python environment are understood,
it is possible to simplify and extend the domain of script usage in batch mode.

The ``ansys.scade.apitools`` module imports the ``scade_env`` module and exposes its ``load_project``
function, which it renames to ``declare_project`` to avoid ambiguities.
Setting the ``PYTHONPATH`` environment variable as specified in the documentation becomes optional.
When the ``PYTHONPATH`` environment variable does not refer to a SCADE environment, the ``ansys.scade.apitools``
module has several strategies to find and dynamically add the required SCADE directories to ``sys.path``,
depending on ``sys.executable``:

* Interpreter delivered in the ``SCADE/contrib/PythonXxx`` directory: The directories are relative to
  the interpretor's location.
* Interpreter of a virtual environment on top of an interpreter delivered with SCADE: The virtual
  environment is resolved. The behavior is then the same as described previously.
* Independent interpreter: The ``ansys.scade.apitools`` module selects the most recent version of SCADE installed on the
  computer that is compatible with the current interpreter:

  * Python 3.7: from 2021 R1 to 2023 R1.
  * Python 3.10: from 2023 R2.

  The behavior is then the same as described previously.

If none of these use cases applies, the script cannot be executed.

This example starts an interactive session with a standard installation of Python:

1. Start an interactive session:

   .. code:: python

       > where python.exe
       C:\Users\jhenry\AppData\Local\Programs\Python\Python310\python.exe
       > python.exe
       Python 3.10.10 (tags/v3.10.10:aad5f6a, Feb  7 2023, 17:20:36) [MSC v.1929 64 bit (AMD64)] on win32
       Type "help", "copyright", "credits" or "license" for more information.

2. Preamble to activate a SCADE environment on a given project.

   .. code:: python

       >>> from ansys.scade.apitools import declare_project
       >>> declare_project(r'C:\Program Files\ANSYS Inc\v232\SCADE\examples\ABC_N\ABC_N.etp')

3. Run a regular script that loads the declared projects and accesses their pathnames.

   .. code:: python

       >>> from scade.model.project.stdproject import get_roots as get_projects
       >>> for project in get_projects():
       ...     print(project.pathname)
       ...
       C:/Program Files/ANSYS Inc/v232/SCADE/examples/ABC_N/ABC_N.etp
