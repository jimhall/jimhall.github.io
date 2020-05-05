---
layout: default
title: Categories
---

<!-- Begin code @ categories/index.md -->

# Category listing

<div class="catcloud">
<!-- Source for sorted categories: https://gist.github.com/Phlow/57eb457898e4ac4c4a20 -->
{% assign sorted_cats = site.categories | sort %}
{%- for category in sorted_cats -%}
  <a href="#{{ category[0] }}"><h3 style="display:inline;">{{ category[0] }}</h3></a>
{% endfor %}
</div>

<p></p>

<div class="catcloud">
{%- for category in sorted_cats -%}
  <a name="{{ category[0] }}"><h3 style="display:inline;">{{ category[0] }}</h3></a>
  <a href="{{ category[0] | prepend: 'categories/' | relative_url }}">
    <h4 style="display:inline;">
        <img src="{{ '/assets/images/arrow-58-32.png' | relative_url }}" width="24" height="24" alt="Dedicated page for {{ category[0] }}">
    </h4>
  </a>
  <ul>
    {%- for post in category[1] -%}
      <li><a href="{{ post.url| relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
<div>

<!-- End code @ categories/index.md -->
