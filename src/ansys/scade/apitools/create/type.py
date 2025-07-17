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
Provide helpers for creating type trees.

Expression trees are intermediate structures to declare any arbitrary complex
types. They create the corresponding SCADE Suite type in the context of a
model element, such as the type of a constant.

This module provides functions to create a type tree for any type of the Scade
language. Thus, the intermediate structures or classes defining the type trees
can be opaque.

Notes: The typing is relaxed in this module to ease the constructs.

* ``TT`` is an alias for ``TypeTree`` to shorten the declarations.

* ``TX``, which stands for extended type tree, is defined as follows::

     Union[str, suite.Type, TT]

  This enhances the usability of these functions by accepting some values,
  such as existing types or name of predefined types, as valid type trees.

"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Union

import scade.model.suite as suite

from .expression import EX, _build_expression
from .scade import _add_pending_link, _get_owner_model


# type trees
class TypeTree(ABC):
    """Provides the top-level abstract class for type trees."""

    @abstractmethod
    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        raise NotImplementedError  # pragma no cover


TT = TypeTree
"""Short name for a ``TypeTree`` instance to simplify the declarations."""

TX = Union[str, suite.Type, TT]
"""Extended type tree to simply the use of the create functions."""


class _Type(TT):
    """Existing type."""

    def __init__(self, type_: suite.Type):
        """Literal value."""
        self.type = type_

    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        return self.type


class _Predefined(TT):
    """Provides the predefined type."""

    def __init__(self, name: str):
        """Initialize a predefined type."""
        self.name = name

    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        return _get_predefined_type(context, self.name)


class _Sized(TT):
    """Provides the sized type."""

    def __init__(self, signed: bool, size: EX):
        self.signed = signed
        self.size = size

    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        type_ = suite.SizedType(context)
        type_.constraint = _get_type_constraint(context, 'signed' if self.signed else 'unsigned')
        type_.size_expression = _build_expression(self.size, context)

        return type_


class _Table(TT):
    """Provides the multi-dimensional array."""

    def __init__(self, dimensions: List[EX], type_: TT):
        self.dimensions = dimensions
        self.type = type_

    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        subtype = self.type._build_type(context) if self.type else None
        for dim in self.dimensions:
            type_ = suite.Table(context)
            type_.size_expression = _build_expression(dim, context)
            _object_link_type(type_, subtype)
            subtype = type_

        return type_


class _Structure(TT):
    """Provides the structure."""

    def __init__(self, fields: List[Tuple[str, TT]]):
        self.fields = fields

    def _build_type(self, context: suite.Object) -> suite.Type:
        """Build a SCADE Suite type from the type tree."""
        type_ = suite.Structure(context)
        elements = []
        for name, subtree in self.fields:
            element = suite.CompositeElement(type_)
            element.name = name
            elements.append(element)
            subtype = subtree._build_type(context) if subtree else None
            _object_link_type(element, subtype)
        type_.elements = elements

        return type_


def _normalize_tree(any: TX) -> TT:
    """Create type tree instances from predefined types or SCADE objects."""
    if any is None or isinstance(any, TT):
        return any
    # SCADE objects
    if isinstance(any, suite.Type):
        return _Type(any)
    # predefined types
    if isinstance(any, str):
        if any == 'bool' or any == 'char':
            return _Predefined(any)
        elif any == 'int' or any == 'real':
            # KCG 6.4 and earlier
            return _Predefined(any)
        elif any in _numeric_types:
            # KCG 6.5 and greater
            return _Predefined(any)
        elif any and any[0] == "'":
            raise _polymorphic_error('_normalize_tree', any)

        else:
            raise _syntax_error('_normalize_tree', any)

    # fall through
    raise _syntax_error('_normalize_tree', any)


def _build_type(tree: TX, context: suite.Object) -> suite.Type:
    """
    Build a type from an extended type tree.

    Parameters
    ----------
    tree : TX
        Type expressed as an extended type tree.
    context : suite.Object
        Context of the creation of the type. This parameter is used to
        create the instances of the types, find the predefined types, or
        resolve polymorphic types (TODO).

    Returns
    -------
    suite.Type
    """
    tree = _normalize_tree(tree)
    return tree._build_type(context)


def create_sized(signed: bool, size: EX) -> TT:
    """
    Get the type tree for a sized type.

    Parameters
    ----------
    signed : bool
        Whether the type is signed.
    size : EX
        Size of the type expressed as an expression tree.

    Returns
    -------
    TT
    """
    if isinstance(size, int) and size not in [8, 16, 32, 64]:
        raise _syntax_error('_create_sized', size)
    return _Sized(signed, size)


def create_table(dimensions: Union[EX, List[EX]], type_: TX) -> TT:
    r"""
    Get the type tree for a structure.

    Parameters
    ----------
    type\_ : TX
        Type tree defining the type of the array elements.
    dimensions : Union[EX, List[EX]]
        Dimensions of the array, which is either a single expression tree or
        a list of expression trees.

    Returns
    -------
    TT
    """
    if not isinstance(dimensions, list):
        dimensions = [dimensions]
    if len(dimensions) == 0:
        raise _syntax_error('_create_table', dimensions)
    type_ = _normalize_tree(type_)
    return _Table(dimensions, type_)


def create_structure(*fields: Tuple[str, TX]) -> TT:
    r"""
    Get the type tree for a structure.

    Notes
    -----
    This is an interface change with respect to the **SCADE Creation Library**.
    The pairs "pattern"/"value" are now embedded in a list of tuples.

    Parameters
    ----------
    \*fields : Tuple[str, TX]
        Name/type expression trees.

    Returns
    -------
    TT
    """
    if len(fields) == 0:
        raise _syntax_error('create_structure', fields)
    normalized_fields = [(_[0], _normalize_tree(_[1])) for _ in fields]
    return _Structure(normalized_fields)


# ----------------------------------------------------------------------------
# Helpers (private)


def _syntax_error(context, tree) -> Exception:
    """Format a dedicated message from the parameters."""
    return ValueError('%s: %s: Type syntax error' % (context, tree))


def _polymorphic_error(context, tree) -> Exception:
    """Format a dedicated message from the parameters."""
    return ValueError('%s: %s: Illegal polymorphic type' % (context, tree))


_predefined_types = {}
"""
Cache for predefined types.

* The key is a name.
* The value is the corresponding predefined type.
"""

_type_constraints = {}
"""
Cache for type constraints.

* The key is a name.
* The value is the corresponding type constraint.
"""

_numeric_types = [
    'int8',
    'int16',
    'int32',
    'int64',
    'uint8',
    'uint16',
    'uint32',
    'uint64',
    'float32',
    'float64',
]
"""List of the numeric types for KCG 6.6."""

_constraints = [
    'numeric',
    'integer',
    'signed',
    'unsigned',
    'float',
]
"""List of constraints."""


def _get_predefined_type(context: suite.Object, name: str) -> suite.NamedType:
    """
    Return a predefined type instance from a name for a given context.

    Parameters
    ----------
    context : suite.Object
        Object from which the owning session can be derived.
    name : str
        Name of the type.

    Returns
    -------
    suite.NamedType
    """
    global _predefined_types

    type_ = _predefined_types.get(name)
    if type_ is None:
        model = _get_owner_model(context)
        session = model.session
        type_ = session.find_predefined_type(name)
        _predefined_types[name] = type_
    return type_


def _get_type_constraint(context: suite.Object, name: str) -> suite.TypeConstraint:
    """
    Get a type constraint instance from a name for a given context.

    Parameters
    ----------
    context : suite.Object
        Object from which the owning session can be derived.
    name : str
        Name of the type.

    Returns
    -------
    suite.TypeConstraint
    """
    global _type_constraints

    constraint = _type_constraints.get(name)
    if constraint is None:
        model = _get_owner_model(context)
        session = model.session
        constraint = session.find_type_constraint(name)
        _type_constraints[name] = constraint
    return constraint


def _object_link_type(object_: suite.TypedObject, type_: suite.Type):
    r"""
    Set the type of an object.

    * For an association object, the type is buffered.
    * For a composition object, the build type is updated immediately when required.

    Parameters
    ----------
    object\_ : suite.TypedObject
        Input object.
    type\_ : suite.Type
        Type of the object.
    """
    if type_:
        global _pending_links

        if not isinstance(type_, suite.NamedType):
            object_.build_type = type_
        _add_pending_link(object_, 'type', type_)
