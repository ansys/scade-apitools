# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-FileCopyrightText: 2023 ANSYS, Inc. All rights reserved.

"""List all the typed objects of the loaded projects."""

import scade
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


def outputln(text):
    scade.output(text + '\n')


class List(Visit):
    def __init__(self, model: suite.Model):
        self.visit(model)

    def visit_typed_object(self, typed_object: suite.TypedObject, *args):
        outputln('("%s", ),' % typed_object.get_full_path())


for session in get_sessions():
    List(session.model)
