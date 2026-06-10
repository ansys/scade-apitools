# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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
Provides additional visitors.

Visitors are a must have as soon as there are hierarchies.
The visitors provided by this module have the same design as the one
delivered with SCADE Suite: ``scade.model.suite.visitors.Visit``.

In a few words, a visitor browses the entire hierarchy of an element.
It is possible to derive a class that redefines the visiting functions of a given class.

Available visitors and targeted Python modules:

* ``DfVisitor``: ARINC 661 definition files (``scade.model.a661.df``)
* ``SdyVisitor``: SCADE Display Specifications (``scade.model.display``)
* ``StandardVisitor``: ARINC 661 standard (``scade.model.a661.standard``)
"""

from .a661visitor import (
    StandardVisitor as StandardVisitor,
)
from .modelvisitor import (
    DFVisitor as DFVisitor,
)
from .sdyvisitor import (
    SdyVisitor as SdyVisitor,
)
