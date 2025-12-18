# Format

The format of the final archive is undecided.

As of now, I am considering the following:
- archive of posts converted to markdown, following the structure shown here by [Alex Seifert](https://blog.alexseifert.com/2024/05/30/a-script-for-exporting-wordpress-to-markdown/). One post per folder
- Postgres DB dump
- eBooks in PDF/epub format. These will likely be compilations of posts rather than one each.

# Postgres DB Dump
This will simply be a dump of the database I've compiled with all of the posts & related info. The least user friendly option, but might prove useful down the line. Using this, the posts could be exported and displayed in any number of ways. Rather than being restricted with simply markdown files.

# Post Archive
```
posts/
    date_post-slug/
        index.md <- post converted from html -> markdown
        meta.json <- post metadata

        images/ <- all downloaded images listed in post
            images
        media/ <- all uploads with post
        OR
        media/ <- all uploads associated with post
            images/
            audio/

meta.json:
    id, published_at, updated_at, author, excerpt, categories, tags

    categories and tags will be lists, likely just the name.

    author gets replaced with author name, maybe and/or id?
```

This will be more for "archival" purposes. Each post will be in it's own folder as seen above. Included will be the post text in a markdown file, the post metadata, as well as any images in the post.

It won't be as user friendly, but it'll be somewhat organized. Will definitely be larger in file size than the database dump, maybe around 1-2GB with all the images.

The markdown might also include some of the metadata as frontmatter, which is intended for static site generators like Jekyll and Hugo.


# eBook/PDF Formats
This will be the most suitable format for >95% of people interested in this archive as a reference. Ken has repeatedly stated that there are no plans for eBooks due to complications with the publisher.

Using Calibre, the posts will be exported as epub and also PDF. Posts and images will be embedded in the files, meaning 1 file = 1 post.

Since there were well over 2,000 posts on the website, having that many individual ebooks will quickly get ridiculous. The plan is to compile books together by category/theme, not that much different from how Ken is doing with the "bookshelf collection". 

The bookshelf collection is doing the following:
- Kingdom of Days (this day in Bruce history): One book per month
- Cover Me (songs Bruce has covered): Books compiled by theme:
    - "Encore!": covers that have appeared in the encore
    - "One Time Only!": covers that have (to date) only appeared once
- Roll of the Dice (Bruce originals): Compiled by album, outtakes included.
- Assorted Others:
    - "Springsteen Christmas": his Christmas covers

Splitting the books into themes are nice, and somewhat necessary due to the sheer amount of writing on the site. Sure, a book with every "on this day" event could be in a single book, it would also be several thousand pages and cost that much in USD. This project is digital, and will be totally free. So page limits/cost is not a concern. That being said, several books at a few hundred "pages" is easier both on me as well as anyone interested in reading the books.