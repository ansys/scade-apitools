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

r"""
Provides accessors for textual pragmas.

A textual pragma is made of an identifier, usually related to a tool, and a text.
The syntax and semantic of the text are specific to each tool.
This library provides sets of accessors for several kinds of textual pragmas:

* Generic pragmas: Any text.
* Core tools pragmas: The text has the form ``<key> [<text>]``. These core
  tools include ``kcg`` and ``mc``.
* JSON pragmas: The text is an arbitrary data formatted as JSON, usually
  a dictionary.

Notes\:

* This module assumes that the pragmas of a model element are unique per
  ``<id>`` or per ``(<id>, <key>)`` for core tools pragmas.
* This module assumes that the value of a pragma that is not present is empty,
  instead of raising an exception. Thus, it automatically removes a pragma
  when its new value is empty.
* This module wraps some existing functions of the SCADE Suite Python API
  that are not documented or listed in the Script Wizard's tables.
* The editing functions return whether the model is modified.
"""

import json
from typing import Optional

import scade.model.suite as suite

# Accessors for all pragmas, either text or XML


def find_pragma(object_: suite.Object, id: str) -> suite.Pragma:
    r"""
    Get the pragma ID of an object.

    See the :ref:`pragma <ex__pragma>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.

    Returns
    -------
    suite.Pragma
        ID of the pragma or ``None`` if not found.
    """
    # return next([_ for _ in object_.pragmas if _.id == id], None)
    return object_.find_pragma(id)


def remove_pragma(object_: suite.Object, id: str) -> bool:
    r"""
    Remove the pragma ID from an object.

    See the :ref:`pragma <ex__pragma>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.

    Returns
    -------
    bool
        ``True`` when the pragma is found, ``False`` otherwise.
    """
    # the implementation differs from the default one to return
    # the modification status
    pragma = object_.find_pragma(id)
    if pragma:
        # remove the pragma from its owner
        # None is a legal value for the underlying implementation
        pragma.object = None  # type: ignore
        return True
    return False


# Accessors for textual pragmas


def get_pragma_text(object_: suite.Object, id: str) -> str:
    r"""
    Get the text of the pragma ID for an object.

    * Return an empty string if the pragma does not exist,
      assuming this is the default value.
    * Raise the ``TypeError`` exception when the pragma exists
      but is not textual.

    See the :ref:`pragma <ex__pragma>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.

    Returns
    -------
    str
        Text of the found pragma or ``""``.
    """
    # the implementation differs from the default one to return None
    # when the found pragma is not textual
    pragma = find_pragma(object_, id)
    if pragma:
        if not isinstance(pragma, suite.TextPragma):
            # raise an exception: design error
            raise TypeError("The pragma %s is not a textual pragma" % id)
        return pragma.text
    else:
        # default value
        return ""


def set_pragma_text(object_: suite.Object, id: str, text: str) -> bool:
    r"""
    Update the pragma ID of an object with a new ID.

    * Delete the pragma when the text is empty.
    * Create a new pragma when no pragma ID exists yet.
    * Return whether the model is modified.

    See the :ref:`pragma <ex__pragma>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.
    text : str
        New ID of the pragma.

    Returns
    -------
    bool
        ``True`` when the model is modified, ``False`` otherwise.
    """
    # the implementation differs from the default one to garbage empty
    # pragmas and return the modification status
    if not text:
        # do not store empty pragmas
        return remove_pragma(object_, id)
    else:
        pragma = find_pragma(object_, id)
        if pragma and not isinstance(pragma, suite.TextPragma):
            # raise an exception: design error
            raise TypeError("The pragma %s is not a textual pragma" % id)
        if not pragma or pragma.text != text:
            # use set_pragma_text iff the text is different
            # else the model can be flagged as modified
            object_.set_pragma_text(id, text)
            return True
        else:
            return False


# Accessors for tool pragmas


def find_pragma_tool(object_: suite.Object, id: str, key: str) -> Optional[suite.TextPragma]:
    r"""
    Get the pragma for an object.

    See the :ref:`pragma_tool <ex__pragma_tool>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.
    key : str
        First token of the pragma.

    Returns
    -------
    suite.TextPragma
        Found pragma or ``None`` if not found.
    """
    for pragma in object_.pragmas:
        if pragma.id == id:
            if not isinstance(pragma, suite.TextPragma):
                # raise an exception: design error
                raise TypeError("The pragma %s is not a textual pragma" % id)
            tokens = pragma.text.split(maxsplit=1)
            if tokens and tokens[0] == key:
                return pragma
    return None


def remove_pragma_tool(object_: suite.Object, id: str, key: str) -> bool:
    r"""
    Remove the pragma from an object.

    See the  :ref:`pragma_tool <ex__pragma_tool>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.
    key : str
        First token of the pragma.

    Returns
    -------
    bool
        ``True`` if the pragma is found, ``False`` otherwise.
    """
    pragma = find_pragma_tool(object_, id, key)
    if pragma:
        # remove the pragma from its owner
        # None is a legal value for the underlying implementation
        pragma.object = None  # type: ignore
        return True
    return False


def get_pragma_tool_text(object_: suite.Object, id: str, key: str) -> Optional[str]:
    r"""
    Get the text of the pragma for an object.

    * Return ``None`` when the pragma does not exist.
    * Raise the ``TypeError`` exception when the pragma exists
      but is not textual.

    See the :ref:`pragma_tool <ex__pragma_tool>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.
    key : str
        First token of the pragma.

    Returns
    -------
    str
        Text of the found pragma or "".
    """
    pragma = find_pragma_tool(object_, id, key)
    if pragma:
        tokens = pragma.text.split(maxsplit=1)
        return tokens[1] if len(tokens) > 1 else ""
    return None


def set_pragma_tool_text(object_: suite.Object, id: str, key: str, text: str) -> bool:
    r"""
    Update the pragma ID which text starts with ``key`` of ``object_`` with ``text``.

    * Create a pragma when no pragma ID if no pragma with the given key exists.
    * Return whether the model is modified.

    See the :ref:`pragma_tool <ex__pragma_tool>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to search for the pragma.
    id : str
        ID of the pragma.
    text : str
        New value of the pragma.
    key : str
        First token of the pragma.

    Returns
    -------
    bool
        ``True`` if the model is modified, ``False`` otherwise.
    """
    pragma = find_pragma_tool(object_, id, key)
    new_text = "%s %s" % (key, text) if text else key

    if pragma:
        if pragma.text == new_text:
            return False
    else:
        pragma = suite.TextPragma()
        pragma.id = id
        pragma.object = object_
    pragma.text = new_text
    return True


# Accessors for JSON pragmas


def get_pragma_json(object_: suite.Object, id: str) -> object:
    r"""
    Deserialize a text pragma containing a JSON document to a Python object.

    See the :ref:`pragma_json <ex__pragma_json>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to get the pragma from.
    id : str
        ID of the pragma.

    Returns
    -------
    object
        Python object corresponding to the JSON document stored in the
        pragma. Returns ``{}`` if there is no pragma or ``None`` if the
        pragma does not contain a valid JSON document.
    """
    text = get_pragma_text(object_, id)
    try:
        return json.loads(text) if text else {}
    except json.JSONDecodeError:
        return None


def set_pragma_json(object_: suite.Object, id: str, data: object) -> bool:
    r"""
    Serialize a Python object to a JSON document in a textual pragma.

    An existing pragma with the same ID is updated with the text
    or deleted if the object is ``None`` or empty.

    See the :ref:`pragma_json <ex__pragma_json>` example.

    Parameters
    ----------
    object\_ : suite.Object
        Element to attach the pragma to.
    id : str
        ID of the pragma.
    data : object
        Python object to serialize to a JSON document.

    Returns
    -------
    bool
        ``True`` if the object is modified, ``False`` otherwise.
    """
    text = json.dumps(data, sort_keys=True).strip("\n") if data else ""
    return set_pragma_text(object_, id, text)
