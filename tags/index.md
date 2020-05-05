---
layout: default
title: Tags
---

<!-- Begin code @ tags/index.md -->

# Tags listing

<div class="catcloud">
<!-- Source for sorted categories: https://gist.github.com/Phlow/57eb457898e4ac4c4a20 -->
{% assign sorted_tags = site.tags | sort %}
{%- for tag in sorted_tags -%}
  <a href="#{{ tag[0] }}"><h3 style="display:inline;">{{ tag[0] }}</h3></a>
  <!-- <a href="{{ tag[0] | prepend: 'tags/' | relative_url }}"><h3 style="display:inline;">{{ tag[0] }}</h3></a> -->
{% endfor %}
</div>

<p></p>

<div class="catcloud">
{%- for tag in sorted_tags -%}
  <a name="{{ tag[0] }}"><h3 style="display:inline;">{{ tag[0] }}</h3></a>
  <a href="{{ tag[0] | prepend: 'tags/' | relative_url }}">
    <h4 style="display:inline;">
      <img src="{{ '/assets/images/arrow-58-32.png' | relative_url }}" width="24" height="24" alt="Dedicated page for {{ tag[0] }}">
    </h4>
  </a>
  <ul>
    {%- for post in tag[1] -%}
      <li><a href="{{ post.url| relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
<div>

<!-- End code @ tags/index.md -->
