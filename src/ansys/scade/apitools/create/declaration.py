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
Provides create functions for Scade model declarations.

* Package
* Type
* Constant
* Sensor
* Operator
"""

from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

import scade.model.suite as suite

from .. import _scade_api
from .expression import EX, _normalize_tree
from .project import _check_object

# from .expression import ET
from .scade import _link_pendings, _link_storage_element, _set_modified
from .type import TX, _build_type, _constraints, _get_type_constraint, _object_link_type


class VK(Enum):
    """Visibility kind."""

    PUBLIC = 'Public'
    PRIVATE = 'Private'


def create_package(
    owner: suite.Package, name: str, path: Optional[Path] = None, visibility: VK = VK.PUBLIC
) -> suite.Package:
    """
    Create a package.

    A package has a name and is either stored in a separate file
    or in its owner's file, if the owner is not the model.

    Parameters
    ----------
    owner : suite.Package
        Owner of the package, which is either the model itself or a package.
    name : str
        Name of the package.
    path : Path | None, default: None
        Path of the file for storing the package. This parameter is optional
        if the package's owner is a package. When the path is ``None`` and the
        owner is the model, the package is stored in the model's default file.
    visibility : VK, default: PUBLIC
        Accessibility of the package, which is either public or private.

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
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'package', package)  # type: ignore
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
    path: Optional[Path] = None,
    visibility: VK = VK.PUBLIC,
    symbol_files: Optional[List[Path]] = None,
) -> suite.NamedType:
    """
    Create a named type.

    A named type has a name and a definition.

    Parameters
    ----------
    owner : suite.Package
        Owner of the type, which is either the model itself or a package.
    name : str
        Name of the type.
    definition : TX
        Definition of the type expressed as a type tree.
    path : Path | None, default: None
        Path of the file for storing the type. This parameter is ignored if the
        owner is a package. When the path is ``None`` and owner is the model, the
        type is stored in the model's default file.
    visibility : VK, default: PUBLIC
        Accessibility of the type.
    symbol_files : List[Path] | None, default: None
        List of symbof files (SSL) associated to the type.

    Returns
    -------
    suite.NamedType
    """
    _check_object(owner, 'create_named_type', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'namedType', named_type)  # type: ignore

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
    owner: suite.Package, name: str, path: Optional[Path] = None, visibility: VK = VK.PUBLIC
) -> suite.NamedType:
    """
    Create an imported named type.

    The type has a name and a definition.

    Parameters
    ----------
    owner : suite.Package
        Owner of the type, which is either the model itself or a package.
    name : str
        Name of the type.
    path : Path | None, default: None
        Path of the file for storing the type. This parameter is ignored if the
        owner is a package. When the path is ``None`` and owner is the model, the
        type is stored in the model's default file.
    visibility : VK
        Accessibility of the type.

    Returns
    -------
    suite.NamedType
    """
    _check_object(owner, 'create_imported_type', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'namedType', named_type)  # type: ignore
    named_type.kind = 'Imported'

    # other properties
    named_type.visibility = visibility.value

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, named_type, path)
    else:
        _set_modified(owner)

    return named_type


def create_enumeration(
    owner: suite.Package,
    name: str,
    values: List[str],
    path: Optional[Path] = None,
    visibility: VK = VK.PUBLIC,
) -> suite.NamedType:
    """
    Create a named type defined by an enumeration.

    The type has a name and a list of values.

    Parameters
    ----------
    owner : suite.Package
        Owner of the type, which is either the model itself or a package.
    name : str
        Name of the type.
    values : List[str]
        List of the enumeration values.
    path : Path | None, default: None
        Path of the file for storing the type. This parameter is ignored if
        the owner is a package. When the path is ``None`` and owner is the model,
        the type is stored in the model's default file.
    visibility : VK
        Accessibility of the type.

    Returns
    -------
    suite.NamedType
    """
    _check_object(owner, 'create_enumeration', 'owner', suite.Package)

    named_type = suite.NamedType(owner)
    named_type.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'namedType', named_type)  # type: ignore

    # other properties
    named_type.visibility = visibility.value

    enumeration = suite.Enumeration(owner)
    constants = []
    for value in values:
        constant = suite.Constant(owner)
        constant.name = value
        constants.append(constant)
    enumeration.values = constants

    _object_link_type(named_type, enumeration)
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, named_type, path)
    else:
        _set_modified(owner)

    return named_type


def add_enumeration_values(
    type_: suite.NamedType, values: List[str], insert_before: Optional[str]
):
    r"""
    Add enumeration values to an enumeration type.

    Parameters
    ----------
    type\_ : suite.NamedType
        Named type defining the enumeration.
    values : List[str]
        List of the enumeration values to add.
    insert_before : str | None
        Insertion point of the values. When this parameter is not ``None``
        and exists, the values are inserted before this value. Otherwise,
        the values are added at the end.
    """
    _check_object(type_, 'add_enumeration_values', 'type_', suite.NamedType)

    enumeration = type_.definition
    _check_object(enumeration, 'add_enumeration_values', 'type_', suite.Enumeration)
    assert isinstance(enumeration, suite.Enumeration)  # nosec B101  # addresses linter

    index = len(enumeration.values)  # default
    if insert_before is not None:
        for value in enumeration.values:
            if value.name == insert_before:
                index = int(value.value_range)
                break

    for value in values:
        constant = suite.Constant(enumeration)
        constant.name = value
        # workaround, use a string
        # TODO: what is this workaround?
        constant.value_range = index
        index = index + 1
        # _scade_api is a CPython module defined dynamically
        _scade_api.add(enumeration, 'value', constant)  # type: ignore
    _set_modified(type_)


def create_constant(
    owner: suite.Package,
    name: str,
    type_: TX,
    value: EX,
    path: Optional[Path] = None,
    visibility: VK = VK.PUBLIC,
) -> suite.Constant:
    r"""
    Create a constant.

    A constant has a name, type, and value.

    Parameters
    ----------
    owner : suite.Package
        Owner of the constant, which is either the model itself or a package.
    name : str
        Name of the constant.
    type\_ : TX
        Definition of the type expressed as a type tree.
    value : EX
        Expression tree defining the value.
    path : Path | None, default: None
        Path of the file for storing the constant. This parameter is ignored if
        the owner is a package. When the path is ``None`` and owner is the model,
        theconstant is stored in the model's default file.
    visibility : VK
        Accessibility of the constant.

    Returns
    -------
    suite.Constant
    """
    _check_object(owner, 'create_constant', 'owner', suite.Package)

    constant = suite.Constant(owner)
    constant.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'constant', constant)  # type: ignore
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
    owner: suite.Package,
    name: str,
    type_: TX,
    path: Optional[Path] = None,
    visibility: VK = VK.PUBLIC,
):
    r"""
    Create an imported constant.

    The constant has a name and a type.

    Parameters
    ----------
    owner : suite.Package
        Owner of the type, which is either the model itself or a package.
    name : str
        Name of the constant.
    type\_ : TX
        Definition of the type expressed as a type tree.
    path : Path, default: None
        Path of the file for storing the constant. This parameter is ignored if
        the owner is a package. When the path is ``None`` and owner is the model,
        the constant is stored in the model's default file.
    visibility : VK
        Accessibility of the constant.

    Returns
    -------
    suite.NamedType
    """
    _check_object(owner, 'create_imported_constant', 'owner', suite.Package)

    constant = suite.Constant(owner)
    constant.name = name
    constant.imported = True
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'constant', constant)  # type: ignore

    # other properties
    constant.visibility = visibility.value

    _object_link_type(constant, _build_type(type_, owner))
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, constant, path)
    else:
        _set_modified(owner)

    return constant


def create_sensor(
    owner: suite.Package, name: str, type_: TX, path: Optional[Path] = None
) -> suite.Sensor:
    r"""
    Create a sensor.

    The sensor has a name and a type.

    Parameters
    ----------
    owner : suite.Package
        Owner of the sensor, which is either the model itself or a package.
    name : str
        Name of the sensor.
    type\_ : TX
        Definition of the type expressed as a type tree.
    path : Path | None, default: None
        Path of the file for storing the constant. This parameter is ignored if the
        owner is a package. When the path is ``None`` and owner is the model, the
        constant is stored in the model's default file.

    Returns
    -------
    suite.Sensor
    """
    _check_object(owner, 'create_sensor', 'owner', suite.Package)

    sensor = suite.Sensor(owner)
    sensor.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'sensor', sensor)  # type: ignore

    # no other properties

    _object_link_type(sensor, _build_type(type_, owner))
    _link_pendings()

    if isinstance(owner, suite.Model):
        _link_storage_element(owner, sensor, path)
    else:
        _set_modified(owner)

    return sensor


def _create_operator(
    owner: suite.Package,
    name: str,
    path: Optional[Path],
    visibility: VK = VK.PUBLIC,
    symbol_file: Optional[Path] = None,
    state: bool = False,
) -> suite.Operator:
    """Core function for creating an operator."""
    _check_object(owner, 'create_operator', 'owner', suite.Package)

    operator = suite.Operator(owner)
    operator.name = name
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(owner, 'operator', operator)  # type: ignore

    # other properties
    operator.visibility = visibility.value
    operator.symbol_file = '' if symbol_file is None else str(symbol_file)
    operator.state = state

    _link_storage_element(owner, operator, path)

    return operator


def create_graphical_operator(
    owner: suite.Package,
    name: str,
    path: Optional[Path],
    visibility: VK = VK.PUBLIC,
    symbol_file: Optional[Path] = None,
    state: bool = False,
) -> suite.Operator:
    """
    Create an operator with a graphical diagram.

    The operator has a name.

    Parameters
    ----------
    owner : suite.Package
        Owner of the operator, which is either the model itself or a package.
    name : str
        Name of the operator.
    path : Path | None, default: None
        Path of the file for storing the operator. This parameter is optional
        if the package's owner is a package. When the path is ``None`` and owner
        is the model, the operator is stored in the model's default file.
    visibility : VK, default: PUBLIC
        Accessibility of the operator.
    symbol_file : Path, default: None
        Path of the file defining the symbol of the operator.
    state : bool, default: False
        Whether the operator is a node.

    Returns
    -------
    suite.Operator
    """
    operator = _create_operator(owner, name, path, visibility, symbol_file, state)

    diagram = suite.NetDiagram(operator)
    diagram.name = operator.name
    diagram.landscape = True
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(operator, 'diagram', diagram)  # type: ignore

    return operator


def create_textual_operator(
    owner: suite.Package,
    name: str,
    path: Optional[Path],
    visibility: VK = VK.PUBLIC,
    symbol_file: Optional[Path] = None,
    state: bool = False,
) -> suite.Operator:
    """
    Create an operator with a textual diagram.

    The operator has a name.

    Parameters
    ----------
    owner : suite.Package
        Owner of the operator, which is either the model itself or a package.
    name : str
        Name of the operator.
    path : Path | None, default: None
        Path of the file for storing the operator. This parameter is optional if
        the package's owner is a package. When the path is ``None`` and owner is
        the model, the operator is stored in the model's default file.
    visibility : VK, default: PUBLIC
        Accessibility of the operator.
    symbol_file : Path | None, default: None
        Path of the file defining the symbol of the operator.
    state : bool, default: False
        Whether the operator is a node.

    Returns
    -------
    suite.Operator
    """
    operator = _create_operator(owner, name, path, visibility, symbol_file, state)

    diagram = suite.TextDiagram(operator)
    diagram.name = operator.name
    diagram.landscape = False
    # _scade_api is a CPython module defined dynamically
    _scade_api.add(operator, 'diagram', diagram)  # type: ignore

    return operator


def create_imported_operator(
    owner: suite.Package,
    name: str,
    path: Optional[Path],
    visibility: VK = VK.PUBLIC,
    symbol_file: Optional[Path] = None,
    state: bool = False,
) -> suite.Operator:
    """
    Create an imported operator.

    The operator has a name.

    Parameters
    ----------
    owner : suite.Package
        Owner of the operator, which is either the model itself or a package.
    name : str
        Name of the operator.
    file : Path
        File defining the imported operator.
    path : Path | None
        Path of the file to store the operator. This parameter is optional if
        the package's owner is a package. When the path is ``None`` and owner
        is the model, the operator isstored in the model's default file.
    visibility : VK, default: Public
        Accessibility of the operator.
    symbol_file : Path | None, default: None
        Path of the file defining the symbol of the operator.
    state : bool, default: False
        Whether the operator is a node.

    Returns
    -------
    suite.Operator
    """
    operator = _create_operator(owner, name, path, visibility, symbol_file, state)
    operator.imported = True

    return operator


class IllegalIOError(Exception):
    """Provides the exception for the wrong IO specification."""

    def __init__(self, context, io, role):
        """Provide a customized message."""
        super().__init__('%s: %s: Illegal %s' % (context, io, role))


class ParamImportedError(Exception):
    """Provides the exception for the wrong imported operator specification."""

    def __init__(self, context, item, text):
        """Provide a customized message."""
        super().__init__('%s: %s%s)' % (context, item, text))


def _get_generic_type(operator: suite.Operator, name: str) -> suite.NamedType:
    """Get the polymorphic type name of operator or create it if it does not exist."""
    type_ = next((_ for _ in operator.typevars if _.name == name), None)
    if type_ is None:
        type_ = suite.NamedType(operator)
        type_.name = name
        operator.typevars.append(type_)
    return type_


def _add_operator_ios(
    operator: suite.Operator,
    ios: List[suite.LocalVariable],
    vars: List[Tuple[str, TX]],
    insert_before: Optional[suite.LocalVariable],
) -> List[suite.LocalVariable]:
    """Core function to create operator I/Os."""
    context = 'add_operator_ios'
    _check_object(operator, context, 'operator', suite.Operator)
    if insert_before is not None:
        _check_object(insert_before, context, 'insert_before', suite.LocalVariable)
        if insert_before.operator != operator:
            raise IllegalIOError(context, insert_before, 'IO')
        index = insert_before.interface_range
    else:
        index = len(ios)

    new_ios = []
    for name, tree in vars:
        if isinstance(tree, str) and len(tree) > 0 and tree[0] == "'":
            type_ = _get_generic_type(operator, tree)
        else:
            type_ = _build_type(tree, operator)
        io = suite.LocalVariable(operator)
        io.name = name
        io.interface_range = index
        ios.append(io)
        _object_link_type(io, type_)

        new_ios.append(io)
        index += 1

    _link_pendings()
    _set_modified(operator)

    return new_ios


def add_operator_inputs(
    operator: suite.Operator,
    vars: List[Tuple[str, TX]],
    insert_before: Optional[suite.LocalVariable] = None,
) -> List[suite.LocalVariable]:
    """
    Add inputs to an operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"type" tree are now embedded in a list of tuples.

    Parameters
    ----------
    operator : suite.Operator
        Input operator.
    vars : List[Tuple[str, TX]]
        Name/type expression trees.
    insert_before : suite.LocalVariable | None, default: None
        Insertion point of the inputs. When this parameter is not ``None``, it is
        an existing input of the operator. The inputs are inserted before this input.
        Otherwise, the inputs are added at the end.

    Returns
    -------
    List[suite.LocalVariable]
        List of added inputs.
    """
    return _add_operator_ios(operator, operator.inputs, vars, insert_before)


def add_operator_hidden(
    operator: suite.Operator,
    vars: List[Tuple[str, TX]],
    insert_before: Optional[suite.LocalVariable] = None,
) -> List[suite.LocalVariable]:
    """
    Add hidden inputs to an operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"type" tree are now embedded in a list of tuples.

    Parameters
    ----------
    operator : suite.Operator
        Input operator.
    vars : List[Tuple[str, TX]]
        Name/type expression trees.
    insert_before : suite.LocalVariable | None, default: None
        Insertion point of the inputs. When this parameter is not ``None``, it is
        an existing hidden input of the operator. The hidden inputs are inserted
        before this input. Otherwise, the hidden inputs are added at the end.

    Returns
    -------
    List[suite.LocalVariable]
        List of the added hidden inputs.
    """
    return _add_operator_ios(operator, operator.hiddens, vars, insert_before)


def add_operator_outputs(
    operator: suite.Operator,
    vars: List[Tuple[str, TX]],
    insert_before: Optional[suite.LocalVariable] = None,
) -> List[suite.LocalVariable]:
    """
    Add outputs to an operator.

    Notes
    -----
    This is an interface change with respect to the *SCADE Creation Library*.
    The pairs "name"/"type" tree are now embedded in a list of tuples.

    Parameters
    ----------
    operator : suite.Operator
        Input operator.
    vars : List[Tuple[str, TX]]
        Name/type expression trees.
    insert_before : suite.LocalVariable | None, default: None
        Insertion point of the outputs. When this parameter is not ``None``, it is
        an existing output of the operator. The outputs are inserted before this input.
        Otherwise, the outputs are added at the end.

    Returns
    -------
    List[suite.LocalVariable]
        List of the added outputs.
    """
    return _add_operator_ios(operator, operator.outputs, vars, insert_before)


def add_operator_parameters(
    operator: suite.Operator,
    parameters: List[str],
    insert_before: Optional[suite.Constant] = None,
) -> List[suite.Constant]:
    """
    Add parameters to an operator.

    Parameters
    ----------
    operator : suite.Operator
        Input operator.
    parameters : List[str]
        Name of the parameters to create.
    insert_before : suite.Constant | None, default: None
        Insertion point of the parameter. When this parameter is not ``None``, it is
        an existing parameter of the operator. The parameters are inserted before
        this parameter. Otherwise, the parameters are added at the end.

    Returns
    -------
    List[suite.LocalVariable]
        List of added parameters.
    """
    _check_object(operator, 'add_operator_parameters', 'operator', suite.Operator)
    if insert_before is not None:
        _check_object(insert_before, 'add_operator_parameters', 'insert_before', suite.Constant)
        if insert_before.operator != operator:
            raise IllegalIOError(add_operator_parameters, insert_before, 'parameter')
        index = insert_before.parameter_range
    else:
        index = len(operator.parameters)

    new_parameters = []
    for name in parameters:
        parameter = suite.Constant(operator)
        parameter.name = name
        parameter.parameter_range = index
        operator.parameters.append(parameter)
        _object_link_type(parameter, _build_type('uint32', operator))

        new_parameters.append(parameter)
        index += 1

    _link_pendings()
    _set_modified(operator)
    return new_parameters


def set_specialized_operator(operator: suite.Operator, imported: suite.Operator):
    """
    Declare a specialization of an imported operator.

    Parameters
    ----------
    operator : suite.Operator
        Specializing operator.
    imported : suite.Operator
        Specialized imported operator.
    """
    _check_object(operator, 'set_specialized_operator', 'operator', suite.Operator)
    _check_object(imported, 'set_specialized_operator', 'imported', suite.Operator)
    if not imported.imported:
        raise ParamImportedError(
            'set_specialized_operator: ', imported.name, ': Illegal imported operator'
        )

    operator.specialized_operator = imported
    _set_modified(operator)


def set_type_constraint(type_: suite.NamedType, name: str):
    r"""
    Set the constraint of a polymorphic type.

    Parameters
    ----------
    type\_ : suite.NamedType
        Input polymorphic type.
    name : str
        Name of the constraint.
    """
    _check_object(type_, 'declare_type_constraint', 'type', suite.NamedType)
    if name not in _constraints:
        raise Exception('%s: Unknown constraint' % name)
    type_.constraint = _get_type_constraint(type_, name)

    _set_modified(type_)
