.. _contribute_SCADE_API_tools:

Contribute
##########

Overall guidance on contributing to a PyAnsys library appears in
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys developer's guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to Ansys SCADE API Tools.

The following contribution information is specific to Ansys SCADE API Tools.

Install in developer mode
-------------------------

Installing Ansys SCADE API Tools in developer mode allows you to modify the
source and enhance it.

#. Clone the ``ansys-scade-apitools`` repository:

   .. code:: bash

      git clone https://github.com/ansys/scade-apitools

#. Access the ``scade-apitools`` directory where the repository has been cloned:

   .. code:: bash

      cd scade-apitools

#. Create a clean Python 3.10 environment and activate it:

   You should use the interpreter delivered with Ansys SCADE. For example,
   ``C:\Program Files\ANSYS Inc\v232\SCADE\contrib\Python310\python.exe``.

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure that you have the latest required build system, documentation, testing,
   and CI tools:

   .. code:: bash

      python -m pip install -U pip     # Upgrading pip
      python -m pip install tox        # Installing tox (optional)
      python -m pip install .[build]   # for building the wheels
      python -m pip install .[tests]   # for testing the package
      python -m pip install .[doc]     # for building the documentation

#. Install the project in editable mode:

   .. code:: bash

      python -m pip install --editable .

#. Use `tox`_ to verify your development installation:

   .. code:: bash

      tox


Test
----
Ansys SCADE API Tools uses `tox`_ for testing. This tool allows you to
automate common development tasks (similar to ``Makefile``), but it is oriented
towards Python development.

Use ``tox``
^^^^^^^^^^^

While ``Makefile`` has rules, ``tox`` has environments. In fact, ``tox`` creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following ``tox`` commands are provided:

- ``tox -e style``: Checks for coding style quality.
- ``tox -e tests``: Checks for unit tests.
- ``tox -e tests-coverage``: Checks for unit testing and code coverage.
* ``tox -e doc``: Checks for the documentation-building process.
   * ``tox -e doc-html``: Builds the HTML documentation.
   * ``tox -e doc-links``: Checks for broken links in the documentation.

Use raw testing
^^^^^^^^^^^^^^^
If required, from the command line, you can call style commands like
`black`_, `isort`_, and `flake8`_. You can also call unit testing commands like `pytest`_.
However, running these commands does not guarantee that your project is being tested in an
isolated environment, which is the reason why tools like ``tox`` exist.

Use ``pre-commit``
^^^^^^^^^^^^^^^^^^
Ansys SCADE API Tools follows the PEP8 standard as outlined in
`PEP 8 <https://dev.docs.pyansys.com/coding-style/pep8.html>`_ in
the *PyAnsys developer's guide* and implements style checking using
`pre-commit <https://pre-commit.com/>`_.

To ensure your code meets minimum code styling standards, run these commands::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  Add License Headers......................................................Passed
  ruff.....................................................................Passed
  ruff-format..............................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  update_examples..........................................................Passed

Build documentation
-------------------
For building documentation, you can run the usual rules provided in the
`Sphinx`_ ``make`` file. Here are some examples:

.. code:: bash

    #  build and view the doc from the POSIX system
    make -C doc/ html && your_browser_name doc/html/index.html

    # build and view the doc from a Windows environment
    .\doc\make.bat clean
    .\doc\make.bat html
    start .\doc\_build\html\index.html

However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html

Distribute
----------
If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install .[build]
    python -m build
    python -m twine check dist/*

Post issues
-----------

Use the `Ansys SCADE API Tools Issues <https://github.com/ansys/scade-apitools/issues>`_
page to submit questions, report bugs, and request new features. When possible, use
these templates:

* Bug, problem, error: For filing a bug report
* Documentation error: For requesting modifications to the documentation
* Adding an example: For proposing a new example
* New feature: For requesting enhancements to the code

If your issue does not fit into one of these template categories, click
the link for opening a blank issue.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

.. LINKS AND REFERENCES

.. _tox: https://tox.wiki/en/4.12.0/
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _wheel file: https://github.com/ansys/scade-apitools/releases