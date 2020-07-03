---
layout: none
---

{%- for category in site.categories -%}
  {{ category[0] | remove: '<p>' | remove: '</p>' }}
{% endfor %}

