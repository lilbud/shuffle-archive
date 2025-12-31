# Ebook Notes
The eventual goal for this project is a series of eBooks which compile all of the sites content.

Before getting to that, each post needs a bit of work before any ebooks are created. The content of each post is stored as HTML, and that HTML needs some cleanup/formatting fixes so that it will be converted properly. These fixes are listed in `fixes.txt`, and the code itself is in `cleanup.py`. Additionally, the `ftfy` library is used to fix some encoding quirks.

Once the HTML is cleaned, we can move on to the next step, which is actually creating the ebooks. I'll admit I had no idea how I'd go about it, and I started looking around for projects which did something similar. Ones that took source HTML, cleaned it up a bit, and spit out ebook files in various formats. After a bit of searching I found `otwarchive`, which is the source for a site named "Archive of Our Own", a somewhat well known website.

What the site is isn't important for this project, there was a [part](https://github.com/otwcode/otwarchive/blob/master/app/models/download_writer.rb) that did prove to be of use. The site hosts "works", and those "works" can be not only viewed on the site but downloaded in various formats like epub, PDF, HTML, and others. They manage this using [Calibre](https://calibre-ebook.com/), more specifically their `ebook-convert` command line tool. This handles the conversion from HTML to the various formats. 

Another project providing inspiration is [StandardEbooks](https://standardebooks.org/), a project which creates ebooks out of public domain works. They don't just throw source HTML in and upload the resulting epub files, but have a series of parsing/formatting tools, as well as a manual of standards. These tools and the manual are used to ensure that every book (no matter source language or format) is presented in a consistent style.

Both projects will be used as inspiration for how I end up creating my ebooks. The StandardEbooks manual will prove useful, but I likely won't follow it as scripture, as I'm working in an entirely different genre. Of the `otwarchive` code, I only plan on using their Calibre command and maybe referencing their output files as a loose template to follow.

## Calibre Settings
--toc-threshold: "0",
--use-auto-toc
--title: Post title,
--title-sort: post title with prefixes removed,
--authors: author name (almost always "Ken Rosen"),
--author-sort: author name, last first,
--comments: post excerpt,
--tags: post tags, helpful in Calibre and other ebook managers,
--pubdate: publish date,
--publisher: "e-street-shuffle" or 'lilbud',
--language: 'english',