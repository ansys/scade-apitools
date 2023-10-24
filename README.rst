Ansys SCADE API Tools
=====================
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black| |doc|

..
   |ansys-scade| image:: https://img.shields.io/badge/Ansys-SCADE-ffb71b?labelColor=black&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://github.com/ansys-scade/
   :alt: Ansys SCADE

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-scade-apitools?logo=pypi
   :target: https://pypi.org/project/ansys-scade-apitools/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-scade-apitools.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-scade-apitools
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/ansys/scade-apitools/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/scade-apitools
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/scade-apitools/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/scade-apitools/actions/workflows/ci_cd.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |doc| image:: https://img.shields.io/badge/docs-apitools-green.svg?style=flat
   :target: https://apitools.scade.docs.pyansys.com
   :alt: Doc


Overview
--------
Ansys SCADE API Tools is an extension library for SCADE Python APIs.

Documentation and Issues
------------------------
For more information, see the `Documentation page`_.

Feel free to post issues and other questions at `apitools Issues`_.
This is the best place to post questions and code.

Installation
------------
The ``ansys-scade-apitools`` package supports only the versions of Python delivered with
Ansys SCADE, starting from 2021 R2:

* 2021 R2 -> 2023 R1: Python 3.7
* 2023 R2 ->: Python 3.10

Ansys SCADE API Tools has two installation modes: user and developer.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing Ansys SCADE API Tools in user mode, make sure you have the latest version of
`pip`_ with:

.. code:: bash

   python -m pip install -U pip

Then, install Ansys SCADE API Tools with:

.. code:: bash

    python -m pip install ansys-scade-apitools

Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing Ansys SCADE apitools in developer mode allows
you to modify the source and enhance it.

.. note::

   Before contributing to the project, please refer to the `PyAnsys Developer's guide`_. You will
   need to follow these steps:

#. Clone the ``ansys-scade-apitools`` repository:

   .. code:: bash

      git clone https://github.com/ansys/scade-apitools

#. Create a fresh-clean Python 3.7 environment and activate it:

   It is advised to use the interpreter delivered with Ansys SCADE, for example
   ``C:\Program Files\ANSYS Inc\v231\SCADE\contrib\Python37\python.exe``.

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure you have the latest required build system and doc, testing, and CI tools:

   .. code:: bash

      python -m pip install -U pip     # Upgrading pip
      python -m pip install tox        # Installing tox (optional)
      python -m pip install .[build]   # for building the wheels
      python -m pip install .[tests]   # for testing the package
      python -m pip install .[doc]     # for building the documentation


#. Install the project in editable mode:

    .. code:: bash

      python -m pip install --editable .

#. Finally, verify your development installation by running:

   .. code:: bash

      tox


Testing
-------

This project takes advantage of `tox`_. This tool allows to automate common
development tasks (similar to Makefile) but it is oriented towards Python
development.

Using tox
^^^^^^^^^

While Makefile has rules, `tox`_ has environments. In fact, ``tox`` creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following environments commands are provided:

- **tox -e style**: will check for coding style quality.
- **tox -e py**: checks for unit tests.
- **tox -e py-coverage**: checks for unit testing and code coverage.
- **tox -e doc**: checks for documentation building process.


Raw testing
^^^^^^^^^^^

If required, from the command line, you can call style commands, including
`black`_, `isort`_, and `flake8`_, and unit testing commands like `pytest`_.
However, this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


Using ``pre-commit``
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool via:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile, such as:

.. code:: bash

    make -C doc/ html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install '.[build]'
    python -m build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
.. _apitools Issues: https://github.com/ansys/scade-apitools/issues
.. _Documentation page: https://apitools.scade.docs.pyansys.com/
.. _wheel file: https://github.com/ansys/scade-apitools/releases
