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

"""Collection of functions to create or update Scade models."""

from enum import Enum

from .expression import (  # _noqa: F401
    EmptyTreeError,
    ExprSyntaxError,
    TypeIdentifierError,
    _build_expression_tree,
    create_activate,
    create_activate_no_init,
    create_binary,
    create_call,
    create_case,
    create_change_ith,
    create_concat,
    create_data_array,
    create_data_struct,
    create_fby,
    create_flatten,
    create_fold,
    create_foldi,
    create_foldw,
    create_foldwi,
    create_higher_order_call,
    create_if,
    create_init,
    create_make,
    create_map,
    create_mapfold,
    create_mapfoldi,
    create_mapfoldw,
    create_mapfoldwi,
    create_mapi,
    create_mapw,
    create_mapwi,
    create_nary,
    create_pre,
    create_prj,
    create_prj_dyn,
    create_restart,
    create_reverse,
    create_scalar_to_vector,
    create_slice,
    create_times,
    create_transpose,
    create_unary,
)

# ignore F401: functions made available for modules, not used here
from .project import (  # _noqa: F401
    create_configuration,
    create_file_ref,
    create_folder,
    create_prop,
    save_project,
)
from .scade import (  # _noqa: F401
    TypePolymorphicError,
    TypeSyntaxError,
    _add_pending_link,
    _build_type_tree,
    _link_pendings,
    _object_link_type,
    save_all,
)