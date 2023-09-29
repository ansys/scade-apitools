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
Creation functions for Scade model declarations.

* Package
* Type
* Constant
* Sensor
* Operator
"""

from enum import Enum
from pathlib import Path
from typing import List

import scade.model.suite as suite

from .. import _scade_api
from .expression import EX, _normalize_tree
from .project import _check_object

# from .expression import ET
from .scade import _link_pendings, _link_storage_element, _set_modified
from .type import TX, _build_type, _object_link_type


class VK(Enum):
    """Either public or private."""

    PUBLIC = 'Public'
    PRIVATE = 'Private'


def create_package(
    owner: suite.Package, name: str, path: Path = None, visibility: VK = VK.PUBLIC
) -> suite.Package:
    """
    Create an instance of Package.

    A package shall have a name and be either stored in a separate file
    or in its owner's file, if the owner is not the model.

    Parameters
    ----------
        owner : suite.Package
            Owner of the package, either the model itself or a package.

        name : str
            Name of the package.

        path: Path
            Path of the file to store the package.

            This parameter is optional if the package's owner is a package.
            When path is None and owner is the model, the package is
            stored in the model's default file.

        visibility: VK
            Accessibility of the package, either public or private.

    Returns
    -------
        suite.Package
    """

    def add_tree_diagram(package, kind):
        diagram = suite.TreeDiagram(package)
        diagram.landscape = True
        diagram.block_kind = kind
        diagram.package = package

    _check_object(owner, 'create_package', 'owner', suite.Package)

    package = suite.Package(owner)
    package.name = name
    _scade_api.add(owner, 'package', package)
    # create the hidden diagrams for tree views
    add_tree_diagram(package, 'Constants')
    add_tree_diagram(package, 'Types')
    add_tree_diagram(package, 'Sensors')

    # other properties
    package.visibility = visibility.value

    _link_storage_element(owner, package, path)

    return package


def create_named_type(
    owner: suite.Package,
    name: str,
    definition: TX,
    path: Path,
    visibility: VK = VK.PUBLIC,
    symbol_files: List[Path] = None,
) -> suite.NamedType:
    """
    Create an instance of NamedType.

    A type shall have a name and a definition.

    Parameters
    ----------
        owner : suite.Package
            Owner of the type, either the model itself or a package.

        name : str
            Name of the type.

        definition: TX
            Definition of the type expressed as a type tree.

        path: Path
            Path of the file to store the type.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the type is
            stored in the model's default file.

        visibility: VK
            Accessibility of the type, either public or private.

    Returns
    -------
        suite.NamedType
    """
    _check_object(owner, 'create_named_type', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    _scade_api.add(owner, 'namedType', named_type)

    # other properties
    named_type.visibility = visibility.value
    # TODO: compute relative paths?
    if symbol_files:
        named_type.symbol_files = [str(_) for _ in symbol_files]

    type_ = _build_type(definition, owner)
    _object_link_type(named_type, type_)
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, named_type, path)
    else:
        _set_modified(owner)

    return named_type


def create_imported_type(
    owner: suite.Package, name: str, path: Path, visibility: VK = VK.PUBLIC
) -> suite.NamedType:
    """
    Create an instance of NamedType.

    A type shall have a name and a definition.

    Parameters
    ----------
        owner : suite.Package
            Owner of the type, either the model itself or a package.

        name : str
            Name of the type.

        path: Path
            Path of the file to store the type.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the type is
            stored in the model's default file.

        visibility: VK
            Accessibility of the type, either public or private.

    Returns
    -------
        suite.NamedType
    """
    _check_object(owner, 'create_imported_type', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    _scade_api.add(owner, 'namedType', named_type)
    named_type.kind = 'Imported'

    # other properties
    named_type.visibility = visibility.value

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, named_type, path)
    else:
        _set_modified(owner)

    return named_type


def create_enumeration(
    owner: suite.Package, name: str, values: List[str], path: Path, visibility: VK = VK.PUBLIC
) -> suite.NamedType:
    """
    Create an instance of NamedType defined by an enumeration.

    A type shall have a name and a list of values.

    Parameters
    ----------
        owner : suite.Package
            Owner of the type, either the model itself or a package.

        name : str
            Name of the type.

        values: List[str]
            List of the enumeration values.

        path: Path
            Path of the file to store the type.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the type is
            stored in the model's default file.

        visibility: VK
            Accessibility of the type, either public or private.

    Returns
    -------
        suite.NamedType
    """
    _check_object(owner, 'create_enumeration', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    _scade_api.add(owner, 'namedType', named_type)

    # other properties
    named_type.visibility = visibility.value

    enum = suite.Enumeration(owner)
    constants = []
    for value in values:
        constant = suite.Constant(owner)
        constant.name = value
        constants.append(constant)
    enum.values = constants

    _object_link_type(named_type, enum)
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, named_type, path)
    else:
        _set_modified(owner)

    return named_type


def add_enumeration_values(type_: suite.NamedType, values: List[str], insert_before: str):
    """
    Add enumeration values to an enumeration type.

    Parameters
    ----------
        type_ : suite.NamedType
            Named type defining the enumeration.

        values: List[str]
            List of the enumeration values to add.

        insert_before: str
            Insertion point of the values.

            When this parameter is not None, and exists, the values are inserted
            before this value. Otherwise, the values are added at the end.

        visibility: str
            Either 'Public' or 'Private'.
    """
    _check_object(type_, 'add_enumeration_values', 'type_', suite.NamedType)

    enum = type_.definition
    _check_object(enum, 'add_enumeration_values', 'type_', suite.Enumeration)

    index = len(enum.values)  # default
    if insert_before is not None:
        for value in enum.values:
            if value.name == insert_before:
                index = value.value_range
                break

    for value in values:
        constant = suite.Constant(enum)
        constant.name = value
        # workaround, use a string
        constant.value_range = str(index)
        index = index + 1
        _scade_api.add(enum, 'value', constant)
    _set_modified(type_)


def create_constant(
    owner: suite.Package, name: str, type_: TX, value: EX, path: Path, visibility: VK = VK.PUBLIC
) -> suite.Constant:
    """
    Create an instance of Constant.

    A constant shall have a name, a type, and a value.

    Parameters
    ----------
        owner : suite.Package
            Owner of the constant, either the model itself or a package.

        name : str
            Name of the constant.

        type_: TX
            Definition of the type expressed as a type tree.

        value: EX
            Expression tree defining the value.

        path: Path
            Path of the file to store the constant.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the constant is
            stored in the model's default file.

        visibility: VK
            Accessibility of the constant, either public or private.

    Returns
    -------
        suite.Constant
    """
    _check_object(owner, 'create_constant', 'owner', suite.Package)

    constant = suite.Constant(owner)
    constant.name = name
    _scade_api.add(owner, 'constant', constant)
    value = _normalize_tree(value)
    constant.value = value._build_expression(owner)

    # other properties
    constant.visibility = visibility.value

    _object_link_type(constant, _build_type(type_, owner))
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, constant, path)
    else:
        _set_modified(owner)

    return constant


def create_imported_constant(
    owner: suite.Package, name: str, type_: TX, path: Path, visibility: VK = VK.PUBLIC
):
    """
    Create an instance of Constant.

    An imported constant shall have a name and a type.

    Parameters
    ----------
        owner : suite.Package
            Owner of the type, either the model itself or a package.

        name : str
            Name of the constant.

        type_: TX
            Definition of the type expressed as a type tree.

        path: Path
            Path of the file to store the constant.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the constant is
            stored in the model's default file.

        visibility: VK
            Accessibility of the constant, either public or private.

    Returns
    -------
        suite.NamedType
    """
    _check_object(owner, 'create_imported_constant', 'owner', suite.Package)

    constant = suite.Constant(owner)
    constant.name = name
    constant.imported = True
    _scade_api.add(owner, 'constant', constant)

    # other properties
    constant.visibility = visibility.value

    _object_link_type(constant, _build_type(type_, owner))
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, constant, path)
    else:
        _set_modified(owner)

    return constant


def create_sensor(owner: suite.Package, name: str, type_: TX, path: Path) -> suite.Sensor:
    """
    Create an instance of Sensor.

    A sensor shall have a name and a type.

    Parameters
    ----------
        owner : suite.Package
            Owner of the constant, either the model itself or a package.

        name : str
            Name of the sensor.

        type_: TX
            Definition of the type expressed as a type tree.

        path: Path
            Path of the file to store the constant.

            This parameter is ignored if the owner is a package.
            When path is None and owner is the model, the constant is
            stored in the model's default file.

    Returns
    -------
        suite.Sensor
    """
    _check_object(owner, 'create_sensor', 'owner', suite.Package)

    sensor = suite.Sensor(owner)
    sensor.name = name
    _scade_api.add(owner, 'sensor', sensor)

    # no other properties

    _object_link_type(sensor, _build_type(type_, owner))
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, sensor, path)
    else:
        _set_modified(owner)

    return sensor
