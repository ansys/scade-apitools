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

"""Collection of functions for the accessing the expressions."""

from enum import Enum

# ignore F401: functions made available for modules, not used here
from .access import (  # _noqa: F401
    ActivateNoInitOp,
    ActivateOp,
    ArrayOp,
    BinaryOp,
    CaseOp,
    ChgIthOp,
    ConstValue,
    DataArrayOp,
    DataStructOp,
    Expression,
    FbyOp,
    FlattenOp,
    IdExpression,
    IfThenElseOp,
    InitOp,
    IteratorOp,
    Label,
    Last,
    ListExpression,
    MakeOp,
    NAryOp,
    NumericCastOp,
    OpCall,
    PartialIteratorOp,
    PreOp,
    Present,
    PrjDynOp,
    PrjOp,
    RestartOp,
    ScalarToVectorOp,
    SharpOp,
    SliceOp,
    TextExpression,
    TransposeOp,
    UnaryOp,
    accessor,
)
from .predef import Eck  # _noqa: F401
