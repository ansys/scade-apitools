Make
====

Overview
--------

Apply a design pattern to an existing project to create new operators and diagrams.

The design pattern used in this example is very simple. It outputs a structure flow
containing pairs made of a default value and a status, depending on the input.

The input model contains the declaration of the output structure as well as
the operator and its interface, with an empty graphical diagram:

.. code-block:: swan

    package MyPackage
        const
            NCD : int32 = 2;
            NORMAL : int32 = 4;

        type
            MyType = {
                element1 : int32,
                element1Status : int32,
                element2 : bool,
                element2Status : int32
            };

        function Root(isMaster : bool)
        returns (out : MyType)
        let
        tel
    end;

The script produces the following diagram:

.. figure:: /examples/create/create_make.png

The content of the script is described exhaustively hereafter.

Import directives and main
--------------------------

The ``main`` function allows the script to be used by the wrapper script::

    import scade.model.suite as suite

    import ansys.scade.apitools.create as create
    import ansys.scade.apitools.query as query


    def main():
        """Apply the design pattern to a given operator."""
        # assume one and only one loaded project
        model = suite.get_roots()[0].model
        # fill the pattern with existing operator/constants
        process_operator(model, 'MyPackage::Root/', 'MyPackage::NORMAL/', 'MyPackage::NCD/')


    if __name__ == "__main__":
        # launched from scade -script
        main()

Checks
------

The ``process_operator`` function retrieves the model elements from
their path and verifies they are consistent with the pattern to apply.

The ``fill_diagram`` function is then called to apply the pattern
and save the model before returning it::

    def process_operator(model: suite.Model, name: str, name_then: str, name_else: str):
        """
        Validate the input model and parameters before applying the pattern.

        Parameters
        ----------
            name : str
                Path of the operator.

            name_then : str
                Path of the constant to be used as status if the input condition is true.

            name_else : str
                Path of the constant to be used as status if the input condition is false.

        """
        # search the model for the operator
        operator = model.get_object_from_path(name)
        if not isinstance(operator, suite.Operator):
            raise ValueError(name + ': Operator not found')

        # get the first diagram of the operator (expect a graphical one)
        diagram = None if len(operator.diagrams) == 0 else operator.diagrams[0]
        if not isinstance(diagram, suite.NetDiagram):
            raise ValueError(name + ': The first diagram is not a net diagram')

        # get the output (expected unique output?)
        output = None if len(operator.outputs) == 0 else operator.outputs[0]
        if output is None:
            raise ValueError(name + ': No output')

        # the output's type must be a structure
        if not query.is_structure(output.type):
            raise ValueError(name + ': Incorrect return type')

        # get the first input (at least one required)
        input = None if len(operator.inputs) == 0 else operator.inputs[0]
        if input is None:
            raise ValueError(name + ': No input')

        # get the constants to be used in the equation
        cst_then = model.get_object_from_path(name_then)
        if not isinstance(cst_then, suite.Constant):
            raise ValueError(name_then + ': Constant not found')
        cst_else = model.get_object_from_path(name_else)
        if not isinstance(cst_else, suite.Constant):
            raise ValueError(name_else + ': Constant not found')

        # create the graphical expressions
        fill_diagram(operator, diagram, input, output, cst_then, cst_else)

        # save the modified files
        create.save_all()


Diagram
-------

The ``fill_diagram`` function creates the equations in the diagram at hard-coded positions.

There are as many textual expressions as there are elements in the structure type.
These are a sequence of (default value, status).

Initialization
^^^^^^^^^^^^^^

Define the positions of the equations and default sizes::

    def fill_diagram(
        operator: suite.Operator,
        diagram: suite.NetDiagram,
        input: suite.LocalVariable,
        output: suite.LocalVariable,
        cst_then: suite.Constant,
        cst_else: suite.Constant,
    ):
        """
        Add the equations to the diagram.

        Parameters
        ----------
            operator : suite.Operator
                Operator to complete.

            diagram : suite.NetDiagram
                Graphical diagram to modify.

            input : suite.LocalVariable
                Input defining the status.

            output : suite.LocalVariable
                Output to define.

            cst_then : suite.Constant
                Constant to be used as status when the input condition is true.

            cst_else : suite.Constant
                Constant to be used as status when the input condition is false.

        """
        # get the structure type
        struct = query.get_leaf_type(output.type)
        count = len(struct.elements)

        # sizes/positions of the different graphical objects used
        x_make = 7000
        y_make = 1000
        w_make = 5000
        element_gap = 650
        h_make = count * element_gap
        # use the default sizes of the SCADE Editor
        w_text = 250
        h_text = 500
        w_output = 300
        h_output = 500

Inputs of the make equation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the equations and cache the defined flows in the ``parameters`` list::

        x_text = x_make - w_text - 1000
        # parameters for make: list of the internal variables defined by the textual expressions
        parameters = []

        for index, field in enumerate(struct.elements):
            # align the input equations with the input pins: trees and intervals...
            y_text = y_make + h_make / (count + 1) * (index + 1) - h_text / 2

            if index % 2:
                # status
                tree = create.create_if(input, cst_then, cst_else)
                eq = create.add_data_def_equation(
                    operator,
                    diagram,
                    ['int32'],
                    tree,
                    (x_text, y_text),
                    (w_text, h_text),
                    textual=True,
                )
                # retrieve the defined variable
                parameters.append(eq.lefts[0])
            else:
                # provide a default value depending on the type, bool or integer in this example
                value = False if query.get_leaf_type(field.type).name == 'bool' else 0
                eq = create.add_data_def_equation(
                    operator, diagram, [field.type], value, (x_text, y_text), (w_text, h_text)
                )
                # retrieve the defined variable
                parameters.append(eq.lefts[0])

Main equation
^^^^^^^^^^^^^

Create the equation for ``make``, using the parameters defined previously::

        tree = create.create_make(output.type, *parameters)
        eq = create.add_data_def_equation(
            operator, diagram, [output.type], tree, (x_make, y_make), (w_make, h_make)
        )
        # retrieve the defined variable
        left_make = eq.lefts[0]

Output
^^^^^^

Create the equation defining the output::

        x_output = x_make + w_make + 2500
        y_output = y_make + h_make / 2 - h_output / 2
        eq = create.add_data_def_equation(
            operator, diagram, [output], left_make, (x_output, y_output), (w_output, h_output)
        )

Edges
^^^^^

Finally, create all the missing edges from the new equations::

        create.add_diagram_missing_edges(diagram)
