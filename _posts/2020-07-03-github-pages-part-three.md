---
layout: post
title: "GitHub Pages 2020: Odds and Ends for a Decent Blog Platform (Part III)"
date: 2020-07-03
categories: [blog, computing, github]
tags: [ghpages, jekyll]
image: "http://www.recursosweb.es/wp-content/uploads/2014/04/github-pages.jpg"
excerpt_separator: <!--more-->
---

This post is some odds and ends which marks the third and final entry on my
journey with GitHub Pages. I am sure it could be argued by someone "Hey do this, do
that" to create a more feature complete blog. Basically, I have invested
enough time with this and what I have delivered with my blog is just enough
for me.

<!--more-->

A vanilla deployment of GitHub Pages does not have much functionality beyond a
secure website deployment that allows you to deploy posts of deep thoughts
without ads. While that was a great lure for me, I had to add a little bit
more functionality to meet my needs. This post captures some of the
modifications to make that happen to my satisfaction, and also tries to
highlight the disparate sources I had to find to make it work (and also try to
credit folks I leveraged to make this work).

Take a look at the [ghpages tag page](https://jimhall.github.io/tags/ghpages)
for all the posts in this series.

## Overall Task Map (checked items in this post)

- [ ] Review relevant GitHub Labs
- [ ] Read/skim the GitHub Pages docs
- [ ] Read/skim the Jekyll docs
- [ ] Get Familiarthe supported Jekyll theme versions and plug-ins
- [ ] Create the GitHub repo for your site (e.g [https://jimhall.github.io](https://jimhall.github.io))
- [ ] Plan out a development model to update your site
- [ ] Theme choice: an aside
- [ ] Create directory structure for blogging
- [ ] Understanding How Pages Get Built
- [ ] Review of `_includes` requirements
- [ ] Review `_layouts` requirements
- [ ] Review `_sass` requirements
- [ ] Create an `index.md`
- [x] Favorite Icon (favicon) Configured
- [x] Add "Essential" Meta Tags
- [x] Generate an RSS Feed
- [x] Allow for Excerpts to be Displayed for Posts
- [x] Add Content to Generate an Archive Page
- [x] Liquid Logic Trick to Reduce Generation of Blank Lines in HTML
- [x] Google Analytics Account Creation
- [x] GitHub Actions: Auto-Generate Tag & Category Pages


## Favorite Icon (favicon) Configured

*Important Sources*:

- https://realfavicongenerator.net/

After hacking away with an image manipulation tool (OmniGraffle), I hacked a
rather pathetic favicon so that when a person accesses the website they will
see my logo in the URL bar. 

Essentially submitted the graphic file to the site and it spits out a bunch of
resized images for the various platforms and browsers. Additionally it
provides some templated meta data that you can see
[here](https://github.com/jimhall/jimhall.github.io/blob/cfc35d415f9b11cb3799a7a49a68926a4e1151c6/_includes/head.html#L10-L20).
I added some liquid (`relative_url`) so that the generated html would have
full URLs (it would not work otherwise).

*SIDE NOTE*: I learned that in order for favicon to work it has to be at the
"base" of the URL (example: https://jimhall.github.io/favicon.ico). The
implication being that if you decide to enable GitHub Pages in a subdirectory
off your base URL (example: https://jimhall.github.io/testrepo) and you place
the favicon in the testrepo directory only it will not work. The favicon will
not replicate to the URL bar of your browser.

## Add "Essential" Meta Tags

*Important Sources*:

- [https://css-tricks.com/essential-meta-tags-social-media/](https://css-tricks.com/essential-meta-tags-social-media/)
- [https://cards-dev.twitter.com/validator](https://cards-dev.twitter.com/validator)

The CSS_TRICKS webpage walks through the various META tags necessary to work
properly with social media sites. My implementation based on this information can be seen in lines 23-28 of
[head.html](https://github.com/jimhall/jimhall.github.io/blob/cfc35d415f9b11cb3799a7a49a68926a4e1151c6/_includes/head.html#L23-L27).

The meta tag `twitter:image` can point to an image that will be seen when post
the web page to twitter. I have also found it has been used by RSS readers
also. My twist is to use some jekyll liquid logic [as
below](https://github.com/jimhall/jimhall.github.io/blob/cfc35d415f9b11cb3799a7a49a68926a4e1151c6/_includes/head.html#L25):

```html
{% raw %}
<meta property="twitter:image" content="{{ page.image | default: "https://jimhall.github.io/assets/images/favicon/apple-touch-icon.png" }}">
{% endraw %}
```

Then I added a [jekyll Front Matter
field](https://jekyllrb.com/docs/front-matter/) called `image:` to each post I want
to have custom image associated with the post. If I do not add the `image:`
field to the post the liquid uses my default [logo image](https://jimhall.github.io/assets/images/favicon/apple-touch-icon.png)

Finally, I used the second source above, the [twitter
validator](https://cards-dev.twitter.com/validator) to see how the image
renders if someone were to tweet my post.

## Generate an RSS Feed

*Important Sources*:

- [https://dzhavat.github.io/2020/01/19/adding-an-rss-feed-to-github-pages.html](https://dzhavat.github.io/2020/01/19/adding-an-rss-feed-to-github-pages.html)
- [https://github.com/jekyll/jekyll-feed#meta-tags](https://github.com/jekyll/jekyll-feed#meta-tags)

RSS is *so* important to me. I believe it is the _killer app_ of the internet
and I am at a loss as to why it is not leveraged more often. I see a lot of
blogs do not even configure an RSS/Atom Feed. I kind of hate social media and
think this would be a great alternative to express ideas.

Enough of the editorial: simply add
[jekyll-feed](https://github.com/jekyll/jekyll-feed) to
`_config.yml` [see source
here](https://github.com/jimhall/jimhall.github.io/blob/master/_config.yml).
This is one of the [supported plug-ins GitHub Pages
offer](https://pages.github.com/versions/). 

From the dzhavat post mentioned above I added the following line to
[head.html](https://github.com/jimhall/jimhall.github.io/blob/master/_includes/head.html):

```html
{% raw %}
<link href="{{ '/feed.xml'| relative_url }}" type="application/atom+xml" rel="alternate"     title="{{ site.title }}"/>
{% endraw %}
```

The use of the `site.title` liquid tag gets dynamically generated with each
post (which is a slight twist on the dzhavat blog).

I added `{% raw %}{% feed_meta %}{% endraw %}` to my
[head.html](https://github.com/jimhall/jimhall.github.io/blob/master/_includes/head.html)
right above the Search Engine Optimization liquid (`{% raw %}{% seo %}{% endraw %}`) and it seems
to work well. See "Meta tags" section of the jekyll-feed documentation (second
source for details.

Important to note: using the "Essential" Meta Tags (see section above) and
using the front matter entry called `image:` in the blog post an RSS news
aggregator will use the image associated with the parameter. 

## Allow for Excerpts to be Displayed for Posts

*Important Sources*:

- [https://jekyllrb.com/docs/posts/#post-excerpts](https://jekyllrb.com/docs/posts/#post-excerpts)

Not much to say here, just follow the docs. Here is a chunk of
[index.md](https://raw.githubusercontent.com/jimhall/jimhall.github.io/master/index.md)
that shows you can use the liquid `{% raw %}{{ post.excerpt }}{% endraw %}` as the posts get lifted
and all the text before `<!--more-->` gets displayed under the URL:

```jekyll
{% raw %}
<ul>
{% for post in site.posts %}
  <li><span>{{ post.date | date_to_string }}</span> » <a href="{{ post.url | relative_url }}" title="{{ post.title }}">{{ post.title }}</a></li>
  {{ post.excerpt }}
{% endfor %}
</ul>
{% endraw %}
```

## Add Content to Generate an Archive Page

*Important Source*:

- [https://www.mitsake.net/2012/04/archives-in-jekyll/](https://www.mitsake.net/2012/04/archives-in-jekyll/)

There seems to be Jekyll plug-ins that would do this work automatically, but
GitHub Pages does not support it at this time. Using the website source at
mitsake.net above I created the following [jekyll logic that organizes the posts by
date](https://raw.githubusercontent.com/jimhall/jimhall.github.io/master/archive/index.md):

```jekyll
{% raw %}
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
{% endraw %}
```

## Liquid Logic Trick to Reduce Generation of Blank Lines in HTML

*Important Sources*:

- [https://talk.jekyllrb.com/t/jekyll-adding-open-and-close-paragraph-to-include-that-should-not-be-there/3872/6](https://talk.jekyllrb.com/t/jekyll-adding-open-and-close-paragraph-to-include-that-should-not-be-there/3872/6)

Just a quick note here: Jekyll `for` loops seem to generate blank lines in the
compiled html for the actual site. Adding a `-` after the opening `%` and
before the closing `%` seemed to help reduce (not eliminate) some of the
unnecessary blank lines. Taking the archive sample above:

```jekyll
{% raw %}
{%- for post in site.posts -%}

...code....

{%- endfor -%}
{% endraw %}
```

## Google Analytics Account Creation

*Important Sources*:

- Used:
  [https://github.com/dwyl/learn-google-analytics](https://github.com/dwyl/learn-google-analytics)
- Also:
  [https://stackoverflow.com/questions/17207458/how-to-add-google-analytics-tracking-id-to-github-pages](https://stackoverflow.com/questions/17207458/how-to-add-google-analytics-tracking-id-to-github-pages)
- [https://desiredpersona.com/google-analytics-jekyll/](https://desiredpersona.com/google-analytics-jekyll/)

Basically followed the steps in the first source to create a Google Analytics
account and used the desiredpersona.com link to decide to add the code to the
[_includes/head.html file](https://github.com/jimhall/jimhall.github.io/blob/cfc35d415f9b11cb3799a7a49a68926a4e1151c6/_includes/head.html#L39-L48)

## GitHub Actions: Auto-Generate Tag & Category Pages

*Important Sources*:
- [https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#specifying-a-python-version](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#specifying-a-python-version)
- [https://www.edwardthomson.com/blog/github_actions_advent_calendar.html](https://www.edwardthomson.com/blog/github_actions_advent_calendar.html)
- [https://www.edwardthomson.com/blog/github_actions_10_path_triggers.html](https://www.edwardthomson.com/blog/github_actions_10_path_triggers.html)
- [https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions#onpushpull_requestpaths](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions#onpushpull_requestpaths)
- [https://stackoverflow.com/questions/57921401/push-to-origin-from-github-action](https://stackoverflow.com/questions/57921401/push-to-origin-from-github-action)
- Sorted cats see:
  [https://gist.github.com/Phlow/57eb457898e4ac4c4a20](https://gist.github.com/Phlow/57eb457898e4ac4c4a20)

One gap in blog functionality with GitHub Pages is creating categories and
tags and having some kind of page generated that will aggregate posts that are
part of a category or tag. There are Jekyll plug-ins that provide this
service, but GitHub pages do not support them. As a work-around, I figured out
a way to create pages that would aggregate categories or tags using GitHub
Actions.

GitHub Actions are powerful. Obviously I am not an expert, but after reading some of the
standard docs mentioned in the sources section above (with a huge shout out to
the edwardthomson.com GitHub Actions advent calendar posts) I came up with a
way to create category and tag pages after each post is uploaded to the GitHub
repository.

Take a look at the [actions source
file](https://github.com/jimhall/jimhall.github.io/blob/master/.github/workflows/main.yml). Here are the highlights of what it tries to do:

- The GitHub Action is initiated when [a file is added to the `_posts`
  directory](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L5-L11).
  Benefit: other blog maintenance / file modifications will not trigger the
  action, only blog posts will trigger the job.
- It chooses to use [Ubuntu and a Python
  version](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L18-L23)
  to run the action
- It [checks out the version of
  Python](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L28-L33)
  per the
  [documentation](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#specifying-a-python-version)
- It then [runs the Python
  script](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L63-L78)
  twice: once for the categories and then again for the tags.
- Finally, it sets two environment variables that are inherited by the final
  task: $NEWCAT and $NEWTAG. The action then [runs some simple shell
  logic](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L81-L92)
  to determine if it is necessary to add the categories or tags to the repo.
 
Here is what the Python script does:

- [Created a baseline
  environment](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/scripts/tags-n-cats.py#L44-L54).
  [Grabbed some command line
  arguments](https://realpython.com/python-command-line-arguments/), set the
  blog site URL, set the encoding, created the Front Matter stencil for the
  category and tag pages, and finally set the location of the temp file that
  will act as the holder of the environment variable that gets used in the
  small shell script in the GitHub Action.
- Kick off the main part of the script by [processing the command line
  switches](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/scripts/tags-n-cats.py#L56-L70)
- Make a call to the
  [missing_dirs](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/scripts/tags-n-cats.py#L26-L41)
  function that fetches the webpage
  [categoriescloud.html](https://jimhall.github.io/categories/categoriescloud.html)
  or [tagscloud.html](https://jimhall.github.io/tags/tagscloud.html) depending
  on the commandline switch. These webpages contain the current list of tags
  or categories on the site. The markdown for these two pages are pretty
  simple. Here it is for categories:

```jekyll
{% raw %}
---
layout: none
---

{%- for category in site.categories -%}
  {{ category[0] | remove: '<p>' | remove: '</p>' }}
{% endfor %}
{% endraw %}
```

And here it is for tags:

```jekyll
{% raw %}
---
layout: none
---

{%- for tags in site.tags -%}
  {{ tags[0] | remove: '<p>' | remove: '</p>' }}
{% endfor %}
{% endraw %}
```
It then does and `ls` of the current tag or categories directory and saves a
set of all the current sub-dirs on the filesystem.

- The script then [creates new sub-directories if
  necessary](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/scripts/tags-n-cats.py#L75-L96)
  by comparing the set of directories on the file system with the set of
  directories fetched from the webpages.
  After creating the sub-directory the script concatenates a simple index.md
  into the newly created sub-directory. 

And that is it! I then have a [template for
categories/index.md](https://github.com/jimhall/jimhall.github.io/blob/master/categories/index.md)
and a [template for
tags/index.md](https://github.com/jimhall/jimhall.github.io/blob/master/tags/index.md)
that allow for the indexing of all the categories and tags dynamically using
Jekyll. Each category or tag has a "jump page" that lists all the posts for an
individual category or tag by date dynamically using Jekyll also.

A quick word of caution: I over engineered the python script at the end
of the day in my opinion. I fetch pages from the site that list the current
categories and tags that have been generated. Then I check the tags and
categories directory to see what has been generated to date. The problem is
that it takes longer for GitHub to generate the new post when added than it
takes to run the GitHub Action. As result I had to add an [arbitray
sleep](https://github.com/jimhall/jimhall.github.io/blob/9f110efedeb46e38d93c75a1ea44336f5ae77c45/.github/workflows/main.yml#L63-L65)
to the action script. If I were to start again, I would just parse the Front
Matter of the blog posts and compare that set of tags to the current directory
strucuture and then proceed with next steps.

And that is how I created the blog by using GitHub Pages. A lot of these ideas
can be leveraged regardless of the Theme you choose. 
