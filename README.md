# Shuffle Archive

More info can be viewed [here](https://lilbud.github.io/2025/12/11/shuffle-archive/).

This repository contains an archive of Ken Rosen's *E Street Shuffle* blog which officially shut down on January 4th 2026.

This archive is being provided as-is. With both the site's content, as well as the various Python code used to compile it. I've tried to document as much as I can, but not entirely.

For a more "accessible" form of the archive, a reproduction has been created and is available here: https://lilbud.github.io/shuffle/

The archive is available in a few forms, all in this repository:

- JSON: JSON files acquired from the sites WP API. These are the "source" for all other formats, and contain all of the data needed for each post.
- Markdown: The post content has been converted to markdown for easy reading.
- PostgreSQL Database Dump: A database compiled from the above JSON files.

Additionally, a Hugo-based recreation of the original ESS site has been created. The repository for that can be found here: https://github.com/lilbud/shuffle

# Formatting Note

As part of the extensive work involved in this archive, nearly every post has had it's formatting fixed to some degree. Only fixing issues present in the source HTML gotten from the API JSON files. An incomplete list of fixes can be found in `notes/fixes.md`.

The work took place over several months, and I didn't do the most complete job documenting *every* little fix. The above file is about as good as it will get.

Fixes to the formatting include adding blockquotes to any long form quoted text (lyrics, speeches, etc.) Additionally, images have been replaced with links to this archive repo instead of estreetshuffle.com. Youtube/Videopress embeds have been changed to direct links. Any Youtube links that needed to be replaced (due to deletion) were replaced and a note was appended prior.
