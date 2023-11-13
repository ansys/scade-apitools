top_level
=========

Overview
--------

Example for creating a top-level operator which calls all existing root operators.

The interface of the top-level operator is the union of the
model's sensors and inputs/outputs of the called operators.

The semantics parts of the example are quite simple.
Most of the statements are related to the computation of positions and sizes.
However, this is not so complex, and one can reuse the example as a
foundation for further scripts.

The input model has the following call graph:

.. figure:: /examples/create/create_top_level_cg.png

The resulting top-level operator is as follows:

.. figure:: /examples/create/create_top_level_root.png

Import directives and main
--------------------------

The function ``main`` allows the script to be used by the wrapper script.
It saves the project and the model before returning.::

    from pathlib import Path

    import scade.model.project.stdproject as std
    import scade.model.suite as suite

    import ansys.scade.apitools.create as create


    def main():
        """Create a top-level operator which calls the existing root operators."""
        # load the SCADE project and model
        # note: the script shall be launched with a single project
        project = std.get_roots()[0]
        model = suite.get_roots()[0].model
        # create the top-level operator instance
        root = add_operator(project, model, 'Root')
        # fill the operator: interfaces and equations
        fill_top_level(model, root)
        # save the created/modified files
        create.save_project(project)
        create.save_all()


    if __name__ == "__main__":
        # launched from scade -script
        main()

Helper for operators
--------------------

This utility function adds an operator to the model, in a separate file
with the same name, and located in the project's directory::

    def add_operator(project: std.Project, model: suite.Model, name: str) -> suite.Operator:
        """
        Add a new operator to the model, and add its separate storage file in the project.

        Parameters
        ----------
            project : std.Project
                Input project.

            model : suite.Model
                Input model.

            name : str
                Name of the operator.

        Returns
        -------
            suite.Operator
        """
        # store the operator in the project's directory
        path = Path(project.pathname).with_name(name + '.xscade')
        # create the operator in the model, assuming it is a node
        operator = create.create_graphical_operator(model, name, path, state=True)
        # add the separate file to the project
        create.add_element_to_project(project, operator)
        return operator

Top-level operator
------------------

The function ``fill_top_level`` is the main function of the example, which
creates the interface and the graphical equations of the new operator.

The algorithm caches the interface of the root operator in two dictionaries,
``map_inputs`` and ``map_outputs``.
The dictionary ``map_inputs`` is initialized with all existing sensors and
then updated with the inputs of the called operators.
When two operators have an input with the same name, only one input is created in the root operator.
It is not accepted to have outputs with same names although this is not checked. ::

    def fill_top_level(model: suite.Model, root: suite.Operator):
        """
        Create the interface of the operator and complete the diagram.

        Parameters
        ----------
            project : std.Project
                Input project.

            model : suite.Model
                Input model.

            name : str
                Name of the operator.

        Returns
        -------
            suite.Operator
        """
        # local cache: top-level inputs by name
        map_inputs = {}
        # local cache: top-level outputs by name
        map_outputs = {}

        # cache the sensors as inputs
        for sensor in model.all_sensors:
            map_inputs[sensor.name] = sensor

        # gather the root operators of the model, ignoring the libraries
        operators = [_ for _ in model.sub_operators if not _.expr_calls and _ != root]

        # 1. interface
        for operator in operators:
            # create the inputs
            for input in operator.inputs + operator.hiddens:
                name = input.name
                if map_inputs.get(input.name):
                    # ignore duplicated inputs or existing sensors
                    continue
                new_inputs = create.add_operator_inputs(root, [(name, input.type)], None)
                map_inputs[name] = new_inputs[0]
            # create the outputs
            for output in operator.outputs:
                name = output.name
                new_outputs = create.add_operator_outputs(root, [(name, output.type)], None)
                map_outputs[name] = new_outputs[0]

        # 2. common positions and sizes based on SCADE Editor's defaults for all calls
        # operator
        x_op = 5000
        y_op = 1000
        w_op = 1800
        # input
        h_in = 500
        w_in = 260
        # output
        h_out = 500
        w_out = 300

        # 3. calls
        # add the equations in the first diagram: there must be one and only one
        diagram = root.diagrams[0]

        for operator in operators:
            inputs = operator.inputs
            outputs = operator.outputs

            in_count = len(inputs)
            out_count = len(outputs)
            # vertical space between the pins of an equation
            io_margin = 100
            h_op = (h_in + io_margin) * max(in_count, out_count) + h_in

            # 3.1. equations for the inputs/sensors (define an internal variable)
            w, h = w_in, h_in
            x = x_op - w - 2000
            parameters = []
            for index, input in enumerate(inputs):
                y = y_op + h_op / (in_count + 1) * (index + 1) - h / 2
                eq = create.add_data_def_equation(
                    root, diagram, [input.type], map_inputs[input.name], (x, y), (w, h)
                )
                # retrieve the defined internal variable
                parameters.append(eq.lefts[0])

            # 3.2. equation for the operator
            # create the expression tree corresponding to a call to an operator
            tree = create.create_call(operator, parameters)
            # get the list of types for each output
            out_types = [_.type for _ in outputs]
            eq = create.add_data_def_equation(
                root, diagram, out_types, tree, (x_op, y_op), (w_op, h_op)
            )
            # retrieve the defined internal variables
            lefts = eq.lefts

            # 3.3. equations for the outputs
            w, h = w_out, h_out
            x = x_op + w_op + 2000
            for index, (output, input) in enumerate(zip(outputs, lefts)):
                y = y_op + h_op / (out_count + 1) * (index + 1) - h / 2
                create.add_data_def_equation(
                    root, diagram, [map_outputs[output.name]], input, (x, y), (w, h)
                )

            # 3.4. propagate the attribute state of the called operator if it is a node
            if operator.state:
                root.state = True

            # 3.5. add an offset for next call
            op_margin = 1000
            y_op += h_op + op_margin

        # 4. create automatically the graphical connections, with default positions
        create.add_diagram_missing_edges(diagram)
