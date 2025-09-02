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

"""Provides a collection of functions for creating or updating Scade models."""

# ignore F401: functions made available for modules, not used here
from .data_def import (  # noqa: F401
    AK,
    DK,
    IT,
    SK,
    TD,
    TK,
    TR,
    IfTree,
    TransitionDestination,
    TransitionTree,
    add_data_def_assertion,
    add_data_def_equation,
    add_data_def_if_block,
    add_data_def_locals,
    add_data_def_net_diagram,
    add_data_def_probes,
    add_data_def_signals,
    add_data_def_state_machine,
    add_data_def_text_diagram,
    add_data_def_when_block,
    add_diagram_edge,
    add_diagram_equation_set,
    add_diagram_missing_edges,
    add_state_machine_state,
    add_state_transition,
    add_transition_equation,
    add_when_block_branches,
    create_if_action,
    create_if_tree,
    create_transition_fork,
    create_transition_state,
    create_when_branch,
    set_variable_default,
    set_variable_last,
)
from .declaration import (  # noqa: F401
    VK,
    IllegalIOError,
    ParamImportedError,
    add_enumeration_values,
    add_operator_hidden,
    add_operator_inputs,
    add_operator_outputs,
    add_operator_parameters,
    create_constant,
    create_enumeration,
    create_graphical_operator,
    create_imported_constant,
    create_imported_operator,
    create_imported_type,
    create_named_type,
    create_package,
    create_sensor,
    create_textual_operator,
    set_specialized_operator,
    set_type_constraint,
)
from .expression import (  # noqa: F401
    EmptyTreeError,
    ExprSyntaxError,
    TypeIdentifierError,
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
    create_numeric_cast,
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
from .project import (  # noqa: F401
    create_configuration,
    create_file_ref,
    create_folder,
    create_prop,
    save_project,
)
from .scade import (  # noqa: F401
    add_element_to_project,
    add_imported_to_project,
    add_simulation_file_to_project,
    save_all,
)
from .type import create_sized, create_structure, create_table  # noqa: F401
