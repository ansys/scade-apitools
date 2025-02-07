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
Provides queries for SCADE Suite types.

The main purpose of this module is to get the nature of a type regardless of its aliases
and not raise an exception if a type is ``None``.
"""

import scade.model.suite as suite

from .. import prop


def get_type_name(type_: suite.Type) -> str:
    r"""
    Get the name of a type or a string representation.

    See the :ref:`get_type_name <ex__get_type_name>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    str
        Name of a type or a string representation.
    """
    if isinstance(type_, suite.NamedType):
        return type_.name
    else:
        return type_.to_string() if type_ else '<null>'


def get_leaf_alias(type_: suite.Type) -> suite.Type:
    r"""
    Get the closest alias of the input's type definition.

    See the :ref:`get_leaf_alias <ex__get_leaf_alias>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    suite.Type
        Closest alias of the input's type definition or the input type
        itself if it is not an alias, such as an instance of ``NamedType``.
    """
    while isinstance(type_, suite.NamedType) and isinstance(type_.type, suite.NamedType):
        type_ = type_.type
    return type_


def get_leaf_type(type_: suite.Type) -> suite.Type:
    r"""
    Get the definition of the input type, bypassing the aliases.

    See the :ref:`get_leaf_type <ex__get_leaf_type>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    suite.Type
        Definition of the input type or the input type itself itself if it
        is not an alias, such as an instance of ``NamedType`` or a predefined
        type. It is not a named type unless it is predefined.
    """
    while isinstance(type_, suite.NamedType) and type_.type:
        type_ = type_.type
    return type_


def get_cell_type(type_: suite.Type, skip_alias=False) -> suite.Type:
    r"""
    Get the type of the elements of an array, optionally multi-dimensional.

    See the :ref:`get_cell_type <ex__get_cell_type>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type, which must be an array.
    skip_alias : bool, default: False
        Whether the aliased arrays are considered as dimensions
        of the input array.

    Returns
    -------
    suite.Type
        Type of the array elements.

    Examples
    --------
    .. code-block:: swan

        type:
            Real = float32;
            Vector = Real ^2;
            Matrix = Vector ^3;

    Applying the ``get_cell_type`` function to a matrix returns a vector
    if ``skip_alias=False``. Otherwise, a Real`` value is returned.

    ..
        ``get_cell_type`` applied to ``Matrix`` returns ``Vector``
        if ``skip_alias`` is ``False`` otherwise ``Real``.

    ..
       container:: twocol

        .. container:: leftside

            .. code-block:: python
                :caption: Direct type

                cell_type = get_cell_type(matrix_type, False)
                print(cell_type.name)
                Vector

        .. container:: rightside

            .. code-block:: python
                :caption: Indirect type

                cell_type = get_cell_type(matrix_type, True)
                print(cell_type.name)
                Real

    """
    # get the underlying array type
    leaf_type = get_leaf_type(type_)
    if not is_array(leaf_type):
        # raise an exception
        raise TypeError("The type %s is not an array" % get_type_name(type_))
    # get the cell type, which must not be an array
    cell_type = leaf_type.type
    if skip_alias:
        # return the first type which is not an array
        while is_array(cell_type):
            cell_type = get_leaf_type(cell_type).type
    else:
        # return the first type which is not an instance of array
        while isinstance(cell_type, suite.Table):
            cell_type = cell_type.type
    return cell_type


def is_array(type_: suite.Type) -> bool:
    r"""
    Determine if the input type is an array.

    See the :ref:`is_array <ex__is_array>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    bool
        ``True`` when the input type is an array, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    return isinstance(leaf_type, suite.Table)


def is_structure(type_: suite.Type) -> bool:
    r"""
    Determine if the input type is a structure.

    See the :ref:`is_structure <ex__is_structure>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    bool
        ``True`` when the input type is a structure, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    return isinstance(leaf_type, suite.Structure)


def is_enum(type_: suite.Type) -> bool:
    r"""
    Determine if the input type is an enumeration.

    See the :ref:`is_enum <ex__is_enum>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    bool
        ``True`` when the input type is a enumeration, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    return isinstance(leaf_type, suite.Enumeration)


def is_predefined(type_: suite.Type) -> bool:
    r"""
    Determine if the input type is predefined.

    See the :ref:`is_predefined <ex__is_predefined>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    bool
        ``True`` when the input type is predefined, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    return isinstance(leaf_type, suite.NamedType) and leaf_type.is_predefined()


def is_imported(type_: suite.Type) -> bool:
    r"""
    Determine if the input type is imported.

    See the :ref:`is_imported <ex__is_imported>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.

    Returns
    -------
    bool
        ``True`` when the input type is imported, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    return isinstance(leaf_type, suite.NamedType) and leaf_type.is_imported()


def is_scalar(type_: suite.Type, target: str = 'C') -> bool:
    r"""
    Determine if the input type is scalar.

    See the :ref:`is_scalar <ex__is_scalar>` example.

    Parameters
    ----------
    type\_ : suite.Type
        Input type.
    target :
        Target language to consider if the input type is imported.
        Options are ``'C'`` and ``'Ada'``.

    Returns
    -------
    bool
        ``True`` when the input type is scalar, ``False`` otherwise.
    """
    # get the underlying definition
    leaf_type = get_leaf_type(type_)
    if isinstance(leaf_type, suite.Table) or isinstance(leaf_type, suite.Structure):
        return False
    if is_imported(leaf_type):
        if target not in ['C', 'Ada']:
            # raise an exception
            raise ValueError("The target '%s' must be 'C' or 'Ada'" % target)
        else:
            return prop.get_pragma_tool_text(leaf_type, 'kcg', '%s:scalar' % target) is not None
    # either an enumeration, a sized type or a predefined type
    return leaf_type is not None and not leaf_type.is_generic()
