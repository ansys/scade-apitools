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
Provides functions for adding elements to a SCADE project (ETP file).

These functions do not check for semantic errors, like adding two files with the same path.
"""

from os.path import abspath
from typing import Any, List, Optional, Tuple, Union

import scade.model.project.stdproject as std


def create_folder(
    owner: Union[std.Project, std.Folder], path: Union[str, List[str]], extensions: str = ''
) -> std.Folder:
    """
    Create a folder.

    A folder has a name and must be either a root folder of a project or
    a subfolder of another folder.

    Parameters
    ----------
    owner : std.Project or std.Folder
        Owner of the folder, which is either the project itself or a folder.
    path : Union[str, List[str]]
        Path to or name of the folder. When a path is provided, the function
        creates the intermediate folders that do not exist.
    extensions: str
        String defining the extensions associated with the folder.

    Returns
    -------
    std.Folder
        Folder with the given path or name if this folder exists.
    """
    _check_object(owner, 'create_folder', 'owner', (std.Project, std.Folder))

    if isinstance(path, str):
        path = [path]
    for name in path[:-1]:
        # create the intermediate folders
        owner = create_folder(owner, name)
    name = path[-1]
    # check for the existence of the folder
    elements = _get_elements(owner)
    for element in elements:
        if isinstance(element, std.Folder) and element.name == name:
            return element

    # not found
    if isinstance(owner, std.Project):
        folder = std.Folder(owner)
        folder.owner = owner
    else:
        # assert isinstance(owner, std.Folder)
        folder = std.Folder(owner.project)
        folder.folder = owner

    folder.name = name
    folder.extensions = extensions

    return folder


def create_file_ref(owner: Union[std.Project, std.Folder], persist_as: str) -> std.FileRef:
    """
    Create file reference.

    A file reference has a pathname and must be a file of either a project or a folder.

    Parameters
    ----------
    owner : std.Project or std.Folder
        Owner of the file, which is either the project itself or a folder.
    persist_as : str
        String representation of the reference to the file to store in the project's file.
        The string can be either a relative reference to the project or an absolute path.

    Returns
    -------
    std.FileRef
    """
    _check_object(owner, 'create_file_ref', 'owner', (std.Project, std.Folder))

    if isinstance(owner, std.Project):
        file_ref = std.FileRef(owner)
        file_ref.owner = owner
    else:
        # assert isinstance(owner, std.Folder)
        file_ref = std.FileRef(owner.project)
        file_ref.folder = owner

    file_ref.persist_as = persist_as

    return file_ref


def create_configuration(owner: std.Project, name: str) -> std.Configuration:
    """
    Create a configuration.

    A configuration has a name and belongs to a project.

    Parameters
    ----------
    owner : std.Project
        Project.
    name : str
        Name of the configuration.

    Returns
    -------
    std.Configuration
    """
    _check_object(owner, 'create_configuration', 'owner', std.Project)

    configuration = std.Configuration(owner)
    configuration.project = owner
    configuration.name = name

    return configuration


def create_prop(
    owner: std.Annotable, configuration: Optional[std.Configuration], name: str, values: List[str]
) -> std.Prop:
    """
    Create a property.

    Properties are attached to a project, folder, or file reference.

    They have a name and a list of values. They can be associated with a configuration.

    Parameters
    ----------
    owner : std.Annotable
        Element to attach the property to.
    configuration : Configuration | None
        Configuration to associate with the property or ``None``.
    name : str
        Name of the property.
    values : List[str]
        Values of the property as a list of strings.

    Returns
    -------
    std.Prop
    """
    _check_object(owner, 'create_prop', 'owner', std.Annotable)
    if configuration is not None:
        _check_object(configuration, 'create_prop', 'configuration', std.Configuration)

    project = owner if isinstance(owner, std.Project) else owner.project

    prop = std.Prop(project)
    prop.entity = owner
    prop.name = name
    prop.values = values

    if configuration is not None:
        prop.configuration = configuration

    return prop


def save_project(project: std.Project):
    """
    Save the project.

    The path of the project is specified in project.pathname.

    Parameters
    ----------
    project : std.Project
        Project to save.
    """
    _check_object(project, 'save_project', 'project', std.Project)
    project.save(project.pathname)


# -----------------------------------------------------------------------------
# Misc.


# not sure this is a good idea... keep this function for tests only?
def _create_empty_project(pathname: str, configuration: str, products: Optional[List[str]] = None):
    """
    Create the smallest project file as possible on the disk.

    This method, which is for advanced usage, can be used to create initial projects
    for running scripts. Typically, you should use one of the SCADE Project Wizards
    to create projects for a given context, such as SCADE Suite or SCADE Test.

    Parameters
    ----------
    pathname : str
        Path of the project.
    configuration : str
        Name of the configuration. A project must have at least one configuration.
    products: List[str] | None, default: None
        List of tags identifying the nature of the project.
        For example, ``SC`` indicates a SCADE Suite project.
    """
    if products is None:
        products = []
    f = open(pathname, 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<Project id="1" oid_count="4" defaultConfiguration="2">\n')
    if len(products) > 0:
        f.write('\t<props>\n')
        f.write('\t\t<Prop id="3" name="@STUDIO:PRODUCT">\n')
        for product in products:
            f.write('\t\t\t<value>{0}</value>\n'.format(product))
        f.write('\t\t</Prop>\n')
        f.write('\t\t<Prop id="4" name="@SCADE:SAVEVERSION">\n')
        f.write('\t\t\t<value>SCADE65</value>\n')
        f.write('\t\t</Prop>\n')
        f.write('\t</props>\n')
    f.write('\t<configurations>\n')
    f.write('\t\t<Configuration id="2" name="{0}"/>\n'.format(configuration))
    f.write('\t</configurations>\n')
    f.write('</Project>\n')


# -----------------------------------------------------------------------------
# Helpers

# def ApplyPropSet(object, context, dict):
#     for att, value in dict.items():
#         try:
#             _scade_api.set(object, att, value)
#         except:
#             # can't raise an error since calling function
#             # is successful and shall return a value
#             print('warning: ' + context + ': Illegal attribute ' + att + '\n')

# class NoneParamError(Exception):
#     def __init__(self, context, name):
#         self.context = context
#         self.name = name
#     def __str__(self):
#         return self.context + ': ' + self.name + ': Illegal empty parameter'

# class NotObjectError(Exception):
#     def __init__(self, context, name, object):
#         self.context = context
#         self.name = name
#         self.object = object
#     def __str__(self):
#         return self.context + ': ' + self.name + ': Illegal parameter ' + str(self.object)

# class BadClassError(Exception):
#     def __init__(self, context, name, cls):
#         self.context = context
#         self.name = name
#         self.cls = cls
#     def __str__(self):
#         return self.context + ': ' + self.name + ': Illegal class ' + str(self.cls)


def _check_object(object_, context: str, name: str, classes: Union[Any, Tuple[Any, ...]]):
    """Check the type of a parameter and raise a ``TypeError`` if it is not correct."""
    if not isinstance(object_, classes):
        cls = type(object_).__name__
        # classes is either a type or a tuple of types
        if isinstance(classes, tuple):
            types = ' or '.join([_.__name__ for _ in classes])
        else:
            types = classes.__name__
        message = '%s: %s: Illegal type %s, must be %s' % (context, name, cls, types)
        raise TypeError(message)


# to be moved to query.project
def _find_file_ref(project: std.Project, pathname: str) -> Optional[std.FileRef]:
    """
    Search a project for a file with the provided path.

    Parameters
    ----------
    project : std.Project
        Input project.
    pathname : str
        Path of the project to search.

    Returns
    -------
    std.FileRef
    """
    path = abspath(pathname)
    for file_ref in project.file_refs:
        if path == abspath(file_ref.pathname):
            return file_ref
    return None


def _get_elements(parent: Union[std.Project, std.Folder]) -> List[std.Element]:
    """
    Get the contained elements of a project or a folder.

    Parameters
    ----------
    parent: Union[std.Project, std.Folder]
        Input project or folder.

    Returns
    -------
    List[std.Element]
    """
    return parent.roots if isinstance(parent, std.Project) else parent.elements


# def FindObject(context: object, name: str, role: str, att):
#     for item in _scade_api.get(context, role):
#         if _scade_api.get(item, att) == name:
#             return item
#     return None
