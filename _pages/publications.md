---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: false
---

{% if site.author.googlescholar %}
  <div class="wordwrap">See also <a href="{{site.author.googlescholar}}"> Prof. Chen's Google Scholar profile</a>.</div>
{% endif %}

{% include base_path %}

{% for post in site.publications %}
  <h2>{{post.title}}</h2>
  {{post.content}}
{% endfor %}
