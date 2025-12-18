# Ebook Notes

Originally, while I had the idea to create ebooks of the sites content. I wasn't entirely sure how to go about it, let alone at the scale needed for this site.

I wasn't going to rely on a paid third party site like Ken recommends, and wanted to use free (and ideally open source) tools instead. Luckily, I remembered [Calibre](https://calibre-ebook.com/). Which is a program used for reading and managing ebook files. It also has a fairly powerful conversion tool, which can convert files to many formats including epub, pdf, azw3, and more.

Calibre also has a command line tool to speed up the conversion process. And a script will likely be included in this repo showing how it is done.

For example, the content of each post (in the JSON file) is stored as HTML. Some cleanup is needed for that HTML so that it will convert to markdown properly. A list of these various fixes are listed in `fixes.md`. Additionally, `ftfy` is used to fix some encoding related quirks.

Once this is done, the resulting HTML can be converted using Calibres `ebook-convert` command line tool. This results in a clean ebook file for each post.

Seeing as there are 2,000 posts, an ebook for each file is overkill. The final ebooks will likely be compiled like the "bookshelf collection".