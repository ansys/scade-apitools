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
Provides numeric values for the ``predef_opr`` attribute from the ``suite.ExprCall``.

For more information, see the SCADE Suite documentation:
``5 Specific Commands for Python Scripting > Access to Predefined Operators in Python Scripts.``
"""

from enum import Enum


class Eck(Enum):
    """Provides an enum of predefined operators."""

    NONE = 1
    AND = 2
    OR = 3
    XOR = 4
    NOT = 5
    SHARP = 6
    PLUS = 7
    SUB = 8
    NEG = 9
    MUL = 10
    REAL2INT = 11
    INT2REAL = 12
    SLASH = 14
    DIV = 15
    MOD = 16
    PRJ = 18
    CHANGE_ITH = 19
    LESS = 20
    LEQUAL = 21
    GREAT = 22
    GEQUAL = 23
    EQUAL = 24
    NEQUAL = 25
    PRE = 26
    WHEN = 28
    FOLLOW = 29
    FBY = 30
    IF = 31
    CASE = 32
    SEQ_EXPR = 33
    BLD_STRUCT = 34
    MAP = 35
    FOLD = 36
    MAPFOLD = 37
    MAPI = 38
    FOLDI = 39
    SCALAR_TO_VECTOR = 40
    BLD_VECTOR = 41
    PRJ_DYN = 42
    MAKE = 43
    FLATTEN = 44
    MERGE = 45
    REVERSE = 46
    TRANSPOSE = 47
    TIMES = 49
    MATCH = 50
    SLICE = 51
    CONCAT = 52
    ACTIVATE = 53
    RESTART = 54
    FOLDW = 55
    FOLDWI = 56
    ACTIVATE_NOINIT = 57
    CLOCKED_ACTIVATE = 58
    CLOCKED_NOT = 59
    POS = 60
    MAPW = 61
    MAPWI = 62
    NUMERIC_CAST = 63
    MAPFOLDI = 64
    MAPFOLDW = 65
    MAPFOLDWI = 66
    LAND = 67
    LOR = 68
    LXOR = 69
    LNOT = 70
    LSL = 71
    LSR = 72
