---
layout: default
title: Welcome to my blog
---

<!-- Begin code @ index.md -->

# Welcome to my blog

I'm glad you are here. Thanks for stopping by!

Send constructive points or constructive criticism by clicking the social links in the
footer. 

<ul>
{% for post in site.posts %}
  <li><span>{{ post.date | date_to_string }}</span> » <a href="{{ post.url | relative_url }}" title="{{ post.title }}">{{ post.title }}</a></li>
  <!-- 
  <p>{{ post.content | strip_html | truncatewords:50 }}</p>
  -->
  {{ post.excerpt }}
{% endfor %}
</ul>

<!-- End code @ index.md -->
