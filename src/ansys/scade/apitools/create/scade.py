# MIT License
#
# Copyright (c) 2023 ANSYS, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Set of helpers for SCADE model creation functions.

* Persistence
* Predefined types
* Type trees
"""

from os.path import abspath
from pathlib import Path

import scade.model.project.stdproject as std
import scade.model.suite as suite

from .. import _scade_api
from .project import _check_object

_modified_files = set()
"""
Set of modified fimes for save_all.

The set is reset once the files are saved.
"""

_pending_links = []
"""
List of pending associations to be set once an object is built.

* Each element of the list is a tuple (src: Object, role: str, link: Object).
* The list is reset by the function link_pendings.
"""


# ----------------------------------------------------------------------------
# Interface


def save_all():
    """Save all the modified files of Scade models."""
    global _modified_files

    for unit in _modified_files:
        unit.save()

    _modified_files = set()


# ----------------------------------------------------------------------------
# Helpers (private)


def _get_owner_model(object_: suite.Object) -> suite.Model:
    r"""
    Return the model owning an object.

    Parameters
    ----------
        object\_ : suite.Object
            Input object.

    Returns
    -------
        suite.Model
    """
    # obvious...
    _check_object(object_, '_get_owner_model', 'obejct_', suite.Object)
    if isinstance(object_, suite.Model):
        return object_
    # shortcut
    if object_.defined_in:
        return object_.defined_in.model
    # the item is not associated to a file, for example a predefined type?
    # --> loop on the owners
    owner = object_.owner
    while owner and not isinstance(owner, suite.Model):
        owner = owner.owner
    return owner


def _get_model_project(model: suite.Model) -> std.Project:
    """
    Return the project adssociated to a model or None if model is a library.

    Note: this is an alternative to model.project which raises a crash in some circumstances.

    Parameters
    ----------
        model : suite.Model
            Input model.

    Returns
    -------
        std.Project
    """
    pathname = abspath(model.descriptor.model_file_name)
    return next((_ for _ in std.get_roots() if abspath(_.pathname) == pathname), None)


def _is_ident(name: str) -> bool:
    """
    Return whether name is a valid identifier.

    Note: the implementation uses ``str.isidentifier`` which accepts
    a superset of Scade identifiers.

    Parameters
    ----------
        name : str
            Name to verify.
    """
    return name.isidentifier()


def _get_default_file(model: suite.Model) -> Path:
    """
    Return the default file to store model level declarations.

    Note: this is either the value of the projet's tool property ``@SCADE:DEFAULTFILE``
    or the path of the model with the suffix ``.xscade``.

    Parameters
    ----------
        model : suite.Model
            Input model.

    Returns
    -------
        str
    """
    # default value
    path = Path(model.descriptor.model_file_name).with_suffix('.xscade')
    # check for an overridden value in the projet's properties
    # model.project may crash in some circumstances
    project = _get_model_project(model)
    if project:
        value = project.get_scalar_tool_prop_def('SCADE', 'DEFAULTFILE', path.name, None)
        # make the path absolute
        path = path.parent / value

    return path


def _link_storage_element(owner: suite.Package, element: suite.StorageElement, path: Path):
    """
    Link a storage element to the storage unit specified by path.

    * The owner is either a package or a model.
    * The storage unit is created if it does not exist

    Note: element can by any model declaration if owner is a model,
    else element must be a package or an operator.

    Parameters
    ----------
        owner : suite.Package
            Owner of the storage element.

        element : suite.StorageELement
            Element to add to the storage unit.

        path: Path
            Path of the storage unit.

    Returns
    -------
        str
    """
    global _modified_files

    # get the parent model (must exist)
    model = _get_owner_model(owner)

    if owner == model and path is None:
        path = _get_default_file(model)

    if path is not None:
        if owner != model:
            directory = Path(owner.defined_in.sao_file_name).parent
            try:
                persist_as = path.relative_to(directory)
            except ValueError:
                persist_as = str(path)
        else:
            persist_as = ''
        unit = _create_unit(model, str(path), persist_as)
        element.storage_unit = unit
        _modified_files.add(unit)
    else:
        assert owner != model
        _set_modified(owner)


def _add_pending_link(object_: suite.Object, role: str, link: suite.Object):
    r"""
    Bufferize the elements of a an association.

    This is used while creating some complex data. Each link from data elements
    shall be create once the complex data is built and connected to its owner.

    Indeed, if an error occurs while creating the data, it can be difficult to
    delete links to already exiting data, for example types.

    Parameters
    ----------
        object\_ : suite.Object
            Source of the association.

        role : str
            Name of the association end.

        link: suite.Object
            Destination of the association.
    """
    global _pending_links

    _pending_links.append((object_, role, link))


def _link_pendings():
    """Flush the pending_links buffer."""
    global _pending_links

    for object_, role, link in _pending_links:
        _scade_api.set(object_, role, link)
    _pending_links = []


def _set_modified(object_: suite.Object):
    r"""
    Tag the file defining the input object as modified.

    Parameters
    ----------
        object\_ : suite.Object
            Input object.
    """
    global _modified_files

    unit = object.defined_in
    unit.sao_modified = True
    _modified_files.add(unit)


def _create_unit(model: suite.Model, path: Path, persist_as: str) -> suite.StorageUnit:
    """
    Add a storage unit to a Scade model if it does not exist.

    Parameters
    ----------
        model : suite.Model
            Scade model.

        path : Path
            Path of the storage unit.

        persist_as: str
            Reference of the file to store in its owner file.

    Returns
    -------
        suite.StorageUnit
    """
    _check_object(model, '_create_unit', 'model', suite.Model)

    global _modified_files

    for unit in model.model_storage_units:
        if Path(unit.sao_file_name) == path:
            _modified_files.add(unit)
            return unit
    unit = suite.StorageUnit(model)
    unit.sao_file_name = pathname
    if persist_as is not None:
        unit.persist_as = persist_as
    unit.model = model
    _modified_files.add(unit)

    return unit
