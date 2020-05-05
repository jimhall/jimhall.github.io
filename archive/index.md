---
layout: archive
title: "Archive"
---

<!-- Begin archive/index.md code -->
<!-- Needed to add a div class below
if this class is removed OR you add a corresponding 
    </div> you wind up with the html list being 
    preformatted. For some reason jekyll is adding a
    corresponding </div> at the end.
-->

<div class="container"> 
<h2>Archives</h2>
<!-- Code below lifted from https://www.mitsake.net/2012/04/archives-in-jekyll/ -->
{%- for post in site.posts -%}
    {% capture month %}{{ post.date | date: '%m%Y' }}{% endcapture %}
    {% capture nmonth %}{{ post.next.date | date: '%m%Y' }}{% endcapture %}
        {% if month != nmonth %}
            {% if forloop.index != 1 %}</ul>{% endif %}
            <h3>{{ post.date | date: '%B %Y' }}</h3><ul>
        {% endif %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    <time>{{ post.date | date: "%e %B %Y" }}</time>
{%- endfor -%}
<!-- End archive/index.md code -->
