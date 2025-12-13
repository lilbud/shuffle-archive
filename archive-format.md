# Format

The format of the final archive is undecided.

I found a number of existing tools which convert Wordpress sites to markdown. Unfortunately, none of them can be used. 

[eiskalteschatten/export-wordpress-to-markdown](https://github.com/eiskalteschatten/export-wordpress-to-markdown) requires the use of the "users" API endpoint, which is not public.

[lonekorean/wordpress-export-to-markdown](https://github.com/lonekorean/wordpress-export-to-markdown) requires an export file created in Wordpress, which only admins can do. This export file is likely similar to the JSON files saved from the API.

Both of these tools function similarly. They both convert posts on the site to markdown, additionally saving post media/images and metadata as well. I like the structure of both, and will do something similar. Each post saved in it's own folder, with images and a `metadata.json` file. This is subject to change.

This will be one part of the archive. I also wish to create ebooks of the sites content. Likely following the template of the official "bookshelf collection" physical books.

This will be done using Calibre (see: `ebook-notes.md` for that info.) Which allows converting HTML to any number of ebook formats.