# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
Provides helpers for SCADE model creation functions.

* Persistence
* Predefined types
* Type trees
"""

from enum import Enum
from os.path import abspath, relpath
from pathlib import Path
from typing import List, Optional, Union

import scade.model.project.stdproject as std
import scade.model.suite as suite

from .. import _scade_api
from .project import _check_object, _find_file_ref, create_file_ref, create_folder

_modified_files = set()
"""
Set of modified fimes for save_all.

The set is reset once the files are saved.
"""

_pending_links = []
"""
List of pending associations to be set once an object is built.

* Each element of the list is a tuple (src: Object, role: str, link: Object).
* The list is reset by the ``link_pendings`` function.
"""


# ----------------------------------------------------------------------------
# Interface


class Sfk(Enum):
    """Provides kinds of simulation files."""

    C = 1  # Source File for C
    OBJECT = 2  # Object File
    MACRO = 3  # Macro File
    TYPE = 4  # Type Definition File
    ADA = 5  # Source File for Ada


def save_all():
    """Save all modified files of Scade models."""
    global _modified_files

    for unit in _modified_files:
        unit.save()

    _modified_files = set()


def add_element_to_project(
    project: std.Project,
    element: suite.StorageElement,
    folder: Optional[std.Folder] = None,
    default: bool = True,
) -> std.FileRef:
    """
    Add the file defining the storage element to the project.

    The file is added if and only if it is not already present.
    If the file is present, the ``folder`` and ``default`` parameters
    are ignored.

    * When the ``folder`` parameter is not ``None``, the file is added to the
      folder specified.
    * When the ``default`` parameter is ``True``, the file is added to either the
      "Model Files" or "Separate Files" folder, depending on the nature of the
      storage unit.
    * Otherwise, the file is added to the project as a root element.

    Parameters
    ----------
    project : std.Project
        Project to modify.
    element : suite.StorageELement
        Element with storage unit to add to the project.
        If the storage unit is not a root element, the added file is
        tagged as ``NONROOT`` for SCADE.
    folder : std.Folder | None, default: None
        Parent folder of the file to add to the project.
    default : bool, default: True
        Whether to add the file to one of the default folders
        for SCADE Suite files.

    Returns
    -------
    std.FileRef
    """
    unit = element.defined_in
    path = unit.sao_file_name
    file_ref = _find_file_ref(project, path)
    if not file_ref:
        if folder:
            parent = folder
        elif default:
            names = ['Model Files']
            if not unit.is_root():
                names.append('Separate Files')
            parent = create_folder(project, names)
        else:
            parent = project
        file_ref = create_file_ref(parent, path)
        # update persist_as to a relative path to the project
        file_ref.set_path_name(path)
        if not unit.is_root():
            file_ref.set_bool_tool_prop_def('SCADE', 'NONROOT', True, False, None)
    return file_ref


def add_imported_to_project(
    project: std.Project,
    element: Union[suite.NamedType, suite.Operator],
    path: str,
    folder: Optional[std.Folder] = None,
    default: bool = True,
) -> std.FileRef:
    """
    Add an imported source file, associated with the SCADE imported element, to the project.

    The file is added if and only if it is not already present.
    If the file is present, the ``folder`` and ``default`` parameters are ignored.

    * When the ``folder`` parameter is not ``None``, the file is added to the
      folder specified.
    * When the ``default`` parameter is ``True``, the file is added to either the
      "External Code" or "External Type Definitions" folder, depending on the nature
      of the element.
    * Otherwise, the file is added to the project as a root element.

    Parameters
    ----------
    project : std.Project
        Project to modify.
    element : Union[suite.NamedType, suite.Operator]
        Imported element.
    path : str
        Path of the file to add to the project.
    folder : std.Folder | None
        Parent folder of the file to add to the project, default: None.
    default : bool, default: True
        Whether to add the file is added to the default folder
        for SCADE Simulation files, according to the element.

    Returns
    -------
    std.FileRef
    """
    if isinstance(element, suite.Operator):
        kind = Sfk.ADA if Path(path).suffix.lower() in ['.adb', '.ads'] else Sfk.C
        prop = 'IMPORTED_NODES'
    else:
        kind = Sfk.TYPE
        prop = 'IMPORTED_TYPES'

    file_ref = add_simulation_file_to_project(project, path, kind, folder, default)

    elements = file_ref.get_tool_prop_def('SCADE', prop, [], None)
    # get the path without the trailing slash, so that the IDE
    # does fail to find the relationship file-element
    elements.append(element.get_full_path().strip('/'))
    file_ref.set_tool_prop_def('SCADE', prop, elements, [], None)

    return file_ref


def add_simulation_file_to_project(
    project: std.Project, path: str, kind: Sfk, folder: Optional[std.Folder] = None, default=True
) -> std.FileRef:
    """
    Add a file to the project and tag it appropriately for the SCADE simulation.

    The file is added if and only if it is not already present.
    If it is present, the parameters folder and default are ignored.

    The file is added to:

    * The specified folder when not None.
    * Or one of the default folders  "External Code" or "External Type Definitions",
      depending on the kind of the file.
    * Otherwise to the project as a root element.

    Parameters
    ----------
    project : std.Project
        Project to modify.
    path : Path
        Path of the file to be added to the project.
    kind: Sfk
        Kind of the added file.
    folder : std.Folder | None, default: None
        Parent folder of the file to add to the project.
    default : bool
        When True, the file is added to the default folder
        for SCADE Simulation files, according to kind.

    Returns
    -------
    std.FileRef
    """
    file_ref = _find_file_ref(project, path)
    if not file_ref:
        if folder:
            parent = folder
        elif default:
            folders = {
                Sfk.C: 'External Code',
                Sfk.OBJECT: 'External Type Code',
                Sfk.MACRO: 'External Definitions',
                Sfk.TYPE: 'External Type Definitions',
                Sfk.ADA: 'External Code',
            }
            parent = create_folder(project, folders[kind])
        else:
            parent = project
        file_ref = create_file_ref(parent, path)
        # update persist_as to a relative path to the project
        file_ref.set_path_name(path)
        values = {
            Sfk.C: 'CS',
            Sfk.OBJECT: 'Obj',
            Sfk.MACRO: 'Macro',
            Sfk.TYPE: 'Type',
            Sfk.ADA: 'AdaS',
        }
        file_ref.set_scalar_tool_prop_def('SIMULATOR', 'FILEKIND', values[kind], '', None)

    return file_ref


# ----------------------------------------------------------------------------
# Helpers (private)


def _get_owner_model(object_: suite.Object) -> suite.Model:
    r"""
    Get the model owning an object.

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
    Get the project adssociated with a model or ``None`` if the model is a library.

    Notes
    -----
    This function is an alternative to ``model.project``, which causes a crash
    in some circumstances.

    Parameters
    ----------
    model : suite.Model
        Input model.

    Returns
    -------
    std.Project
    """
    pathname = abspath(model.descriptor.model_file_name)
    projects: List[std.Project] = std.get_roots()
    return next((_ for _ in projects if abspath(_.pathname) == pathname), None)


def _get_default_file(model: suite.Model) -> Path:
    """
    Get the default file to store model-level declarations.

    Notes
    -----
    This function returns either the value of the projet's tool property, ``@SCADE:DEFAULTFILE``,
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


def _link_storage_element(
    owner: suite.Package,
    element: suite.StorageElement,
    path: Optional[Path] = None,
):
    """
    Link a storage element to the storage unit specified by a path.

    * The owner is either a package or a model.
    * The storage unit is created if it does not exist

    Notes
    -----
    The element can by any model declaration if the owner is a model.
    Otherwise, the element must be a package or an operator.

    Parameters
    ----------
    owner : suite.Package
        Owner of the storage element.
    element : suite.StorageELement
        Element to add to the storage unit.
    path : Path | None, default: None
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
            persist_as = str(Path(relpath(abspath(path), directory)).with_suffix(''))
        else:
            persist_as = ''
        unit = _create_unit(model, path, persist_as)
        element.storage_unit = unit
        _modified_files.add(unit)
    if owner != model:
        _set_modified(owner)


def _add_pending_link(object_: suite.Object, role: str, link: suite.Object):
    r"""
    Buffer the elements of an association.

    This function is used while creating some complex data. Each link from data elements
    is created once the complex data is built and connected to its owner.

    Indeed, if an error occurs while creating the data, it can be difficult to
    delete links to already exiting data, such as types.

    Parameters
    ----------
    object\_ : suite.Object
        Source of the association.
    role : str
        Name of the association end.
    link : suite.Object
        Destination of the association.
    """
    global _pending_links

    _pending_links.append((object_, role, link))


def _link_pendings():
    """Flush the pending links buffer."""
    global _pending_links

    for object_, role, link in _pending_links:
        # _scade_api is a CPython module defined dynamically
        _scade_api.set(object_, role, link)  # type: ignore
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

    unit = object_.defined_in
    if unit:
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
        if abspath(unit.sao_file_name) == abspath(path):
            _modified_files.add(unit)
            return unit
    unit = suite.StorageUnit(model)
    unit.sao_file_name = str(path)
    unit.persist_as = persist_as
    unit.model = model
    _modified_files.add(unit)

    return unit
