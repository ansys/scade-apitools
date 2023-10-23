{% if false %}
{{ name | escape | underline}}
{% else %}
{# alternative to fullname to have a shorter line #}
{{ objname | escape | underline}}

Module: *{{ module }}*
{% endif %}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:
   :inherited-members:

   {% block methods %}
   ..
      automethod:: __init__

   {% if methods and methods != [_('__init__')] %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
   {% if item != _('__init__') %}
      {{ name }}.{{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock methods %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}

   {% for item in attributes %}
   ..
      autoattribute:: {{ objname }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock attributes %}
