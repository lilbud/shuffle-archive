This file will contain notes about the folder structure of this archive.

Currently, the bulk of the archive is a "Posts" folder with 2k+ JSON files. The files are named with the post ID, and the "lastmodified_gmt" value as a unix timestamp, which isn't easy to convert.

Thought more and more about a proper "structure", ideally one folder per post, and each folder has everything associated with a given post. This would include all media. Additionally, the post will be saved as an HTML file, and likely also markdown (with metadata as YAML front matter). The original JSON will also be included.

Only the latest "true" version of each post will be included in this structure. Many posts are being overwritten, replacing the content and title while keeping ID and URL. Usually the "published" date is updated as well, which makes telling them apart easy. Some might have same slug/title and date, will deal with these on a case by case basis.

Planned structure:
```
Assets/
    images
    audio clips

Archive/
    Posts/
        YYYY-MM-DD-post_slug/
            meta.json # original JSON file from API
            [slug].md # post converted to markdown, inc. meta as front matter
            [slug].html # post as HTML, this will act as the "source" for markdown and also eBook files.
```

As for media, all of those files will be stored in a top level "Assets" folder. I considered storing media with each post, but if certain assets are used in multiple posts then those files will be duplicated. Keeping everything in a single folder reduces the need for duplication.

There will also be an expansion of the "media" table in the database which will list the filenames and the specific post id they're associated with.