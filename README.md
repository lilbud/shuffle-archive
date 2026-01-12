# Shuffle Archive

More info can be viewed [here](https://lilbud.github.io/2025/12/11/shuffle-archive/).

This repo contains a work in progress archive of Ken Rosen's "E Street Shuffle" site. Which has announced it will be shutting down in early 2026. Unfortunately, the shut down has started already, and many posts have since been deleted. I only started archiving on November 30th, I believe this predates much of the deletion process.

As of writing this, the format for the archive will be the following:
- RAW JSON Files: JSON files acquired from the sites WP API. These are the "source" for all other formats, and contain all of the data needed for each post.
- Markdown Files: Each post will be exported as a markdown file, which will be much more readable. Will likely follow the "Jekyll" format, folder for each post with all the media included. Each post will contain the metadata as YAML front matter. Original JSON will be included as a "metadata" file.
- eBook Files: This is intended as the "primary" format for this archive. Posts will be compiled by category/theme, and released as eBook files. Very much a moving target, and details will change as I don't have all of them sorted. I found [StandardEBooks](https://standardebooks.org/), which provide a toolset for creating eBooks easily, and a standard to reference. Will likely provide "inspiration" rather than a hard guide to follow exactly.
- Postgres Database Dump: The posts have been converted from those JSON files to a Postgres database. A dump will be included.

As mentioned, the site will stop being updated in early 2026 (current date is January 5th). The site plans to be live until sometime in 2027/28, but with the ongoing Bookshelf Collection and subsequent post deletion, it will slowly become less useful.

Here is a count of the posts so far, as of 12/23/25 at 12pm:

| Category | Post Count |
| --- | ----------- |
| LA 83 | 0 |
| Once Only | 0 |
| Letter | 0 |
| Hearts of Stone | 1 |
| Two Faces | 3 |
| Holiday | 13 |
| Tunnel | 13 |
| Spare Parts | 22 |
| Uncategorized | 23 |
| Greetings | 35 |
| Encore | 41 |
| Where the Band Was | 77 |
| Meeting Across the River | 352 |
| Kingdom of Days | 393 |
| Roll of the Dice | 587 |
| Cover Me | 967 |

## Note about updated posts (12/24)
In checking some of the posts that are still live have been entirely replaced in some way, but the URL and post ID remains the same. Usually the title and content are completely new, sometimes the modified date as well.

These posts will have the ID, and the "modified at" timestamp appended. These posts will also be included in the database dump.

## Missing Posts (1/10/26)
While sorting through posts to compile these books, I found that 3 posts are completely missing in their original form. All three were replaced back in November before I started archiving the site. They are NOT present on archive.org.

Those posts are:
- Blogger’s Note: Kingdom of Days (2019-01-13)
    - Replaced with Visitation at Fort Horn
- Blogger’s Note: Important Update (2019-04-11)
    - Replaced with Cover Me book intro
- Blogger’s Note: Video omissions in daily e-mails (2021-07-16)
    - Replaced with Roll of the Dice intro

