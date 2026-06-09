These files differ from the documentation to match the Python APIs, from 2023 R1 to 2026 R1.

Removals:
* model.ecore
  * `BCDIntPropValue`
* a661.ecore
  * `MsgPaddingElement`

Renamings:
* a661.ecore
  * A661Layer.runtime -> A661Layer.runtime_messages
  * ArrayElement.fields -> ArrayElement.elements
  * DefinitionPropSelector.bitfield -> DefinitionPropSelector.bit_field
  * Dimension.dimension_element -> Dimension.dimension
  * MsgType.substitutes -> MsgType.subst

The A661 visitors are generated with respect to 2023 R1 ecore models.
