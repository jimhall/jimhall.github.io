---
layout: post
title: "GitHub Pages 2020: Getting Started (Part I)"
date: 2020-06-29
categories: [blog, computing, github]
tags: [ghpages, jekyll, ghlabs]
image: "https://jimhall.github.io/assets/images/1st-issue.png"
excerpt_separator: <!--more-->
---

In what I believe to be a very "meta move", my first blog post will
be about how I created this blog. I found creating this site to be
a trivial activity, but as with a lot of things in life, the first
80% was the easy part.


<!--more-->

The last 20% then turned into consumption of a lot of "spare time"
reading random blog posts and code to get comfortable with
publishing something. This post is part of series that documents
the journey, in the hopes that it will be easier for others.

Take a look at the [ghpages tag page](https://jimhall.github.io/tags/ghpages)
for all the posts in this series.

## Overall Task Map (checked items in this post)

- [x] Review relevant GitHub Labs
- [x] Read/skim the GitHub Pages docs
- [x] Read/skim the Jekyll docs
- [x] Get Familiarthe supported Jekyll theme versions and plug-ins
- [x] Create the GitHub repo for your site (e.g [https://jimhall.github.io](https://jimhall.github.io))
- [x] Plan out a development model to update your site
- [ ] Theme choice: an aside
- [ ] Create directory structure for blogging
- [ ] Understanding How Pages Get Built
- [ ] Review _includes requirements
- [ ] Review _layouts requirements
- [ ] Review _sass requirements
- [ ] Create an index.md
- [ ] Favorite Icon (favicon) Configured
- [ ] Add "Essential" Meta Tags
- [ ] Generate an RSS Feed
- [ ] Allow for Excerpts to be Displayed for Posts
- [ ] Add Content to Generate an Archive Page
- [ ] Liquid Logic Trick to Reduce Generation of Blank Lines in HTML
- [ ] Google Analytics Account Creation
- [ ] GitHub Actions: Auto-Generate Tag & Category Pages

## Why Pick GitHub Pages and First Steps

### Why GitHub Pages?

My reasoning for choosing GitHub Pages is as follows:

- Opportunity to learn git and I liked the appeal of having the blog under source
  code control
- Free with no goofy ads interspersed across the pages
- Secure: specifically use of SSL out of the box without me managing certs
- No wish to manage any infrastructure on my part
- No DNS to manage with a reasonable name for the blog.
- GitHub Gist integration using a Jekyll plug-in _built in_ to GitHub Pages.

### Leverage GitHub Labs

As I started looking at using GitHub, I got a wee-bit overwhelmed with all the
websites and youtube videos trying to sort things out with git and GitHub
pages.

Luckily I will not be writing up yet another git & GitHub Pages 101 blog page. I recommend
that you leverage the following three [GitHub Labs](https://lab.github.com):

- [Introduction to GitHub](https://lab.github.com/githubtraining/introduction-to-github)

The lab focused on the basics of git in an interactive way: create clone, edit
files, commit changes, push to the repo and open a pull request. Options to
use either the website or ssh // command line.

- [Communicating using Markdown](https://lab.github.com/githubtraining/communicating-using-markdown)

Quick Markdown basics course.

- [GitHub Pages](https://lab.github.com/githubtraining/github-pages)

This lab covered how to enable GitHub Pages, choose themes, YAML front matter, create and edit
blog posts. Then keep this page on [Markdown
handy](https://guides.github.com/features/mastering-markdown/)

There was a minimal time investment (about 30 minutes a lab) and it was
enough to at least get going.

### Read/skim the GitHub Pages Documentation

The [GitHub Pages documentation](https://help.github.com/en/github/working-with-github-pages) is
pretty good. I just powered through it all and certainly did not absorb all
the information. I also hopped around a bit and punted to the Jekyll docs a
bit (see below) but some stuff stuck in this old brain.

### Read/skim the Jekyll Documentation

Similar to the GitHub pages documentation, power through the [Jekyll
Documentation](https://jekyllrb.com/docs/). The docs did touch on some of the
key things about Front Matter and Liquid Tags, but I did find that a lot of
the problems I had with developing this site required that I hit up Google and
StackOverflow for answers.

### Get Familiar with the Supported Jekyll Theme Versions and plug-ins

VERY IMPORTANT: Review the [GitHub Dependency versions](https://pages.github.com/versions/). Two key things to get smart on:

- Get familiar with the theme version that you pick for your site. For
  example, when I started this blog with "hacker theme" for this site, I
  sorted out that it is called is called
  [jekyll-theme-hacker](https://rubygems.org/gems/jekyll-theme-hacker) and it
  is at release 0.1.1 at the time of writing. Get familiar and bookmark the
  repo that you choose. You will likely hit display bugs and you will want to
  refer to the source on occasion. Also you may want to understand the
  differences between the verision supported by GitHub pages versus what is
  available on HEAD/master.
- Try to get a sense of the various Jekyll plug-ins. You do not have to be a
  Ruby expert (one huge positive out of this experience is that in spite of
  the challenges and bugs I hit, *none* resulted in me touching any ruby).
  Just try to understand what each plug-in is doing at a high 
  level so you can potentially apply it to your blog site.

### Create the GitHub repo for your site

At the time of this writing, review [this intro
page](https://pages.github.com) on creating your _username_.github.io page.
Really straight forward to at least get started.


### Plan out a development model to update your site

The best practice suggested by GitHub Pages for development of your site is
to:

- Clone a copy of the repo onto the desktop you will develop on
- Install a copy of Jekyll on your local system and all the plug-ins being
  used. This includes getting Ruby up and running.
- Create your content and use your browser to view how the pages are rendering
  and when satisfied push/upload the content to GitHub and make sure it works
  there

I did not do this. I simply created _another_ repo,
[TestBlog4](https://jimhall.github.io/TestBlog4), ```git clone``` that to my
desktop and created my content (and eventually the entire site including
changes to the theme). I found this easier than mangaging an install on my
laptop. It also eliminates the "what changed? -- my laptop or GitHub?".

So that is the baseline. There is a chance that if you follow the step above
about creating the base website, and already understand git, you will not have
to go to crazy on reviewing the documentation, you could dive into my next
post and just get going with blogging with GitHub Pages. Create a _posts
directory and start posting content to GitHub Pages.
