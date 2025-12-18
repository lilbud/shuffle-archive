https://developer.wordpress.org/rest-api/reference/posts/

This is an assortment of notes and observations about the Wordpress API on estreetshuffle.com. This is the method I used to archive much of the site.

# Notes
## Meta and Content
`date` is based on the site's timezone, which is PST. `date` is also listed in GMT, which is the same as UTC.

`modified` and `modified_gmt` are the same as date above. Last edit of the post. Could be used to compare older versions of the same post? Specifically those archived by IA.

`guid > rendered` is a short link to the posts page. More convienent than the "link".

`slug` should be used for filename, optionally appended with the date in timestamp form.

`content > rendered`: the actual content of the post stored in HTML. Some fixes are needed before it will convert cleanly to Markdown or other formats. 

`excerpt > rendered` is the same as content, also in HTML. This may or may not be an abbreviated version of content.

## Media
`featured_media`: ID linking to an image file. A link to the endpoint with that ID can be found under `_links > wp:featuredmedia > href`.

The featured image can also be found under `jetpack_featured_media_url`, without needing to hit the API for every single post.

Images in the post are included in the `content > rendered` item. It's HTML and they're all as `<img>` tags. Those should be downloaded and somehow included with the final archive.

## Comments
`comment_status` can be "open" or "closed". Comments can be gotten using the `_links > replies[0] > href` url. Likely replace this with the saved replies.

Maybe add a "comments" item and set it to the replies gotten using the above endpoint.

## Categories
`categories` are stored in a list of integers, each of which references a specific category name and link. Categories have been included in this repo in the `categories.json` file.

These should be replaced by the category objects.

## Tags
Largely the same as categories. List of integers which reference a tag. A `tags.json` is in this repo with all the tags. Much easier than pinging the API for each one.

These should be replaced with the tag objects.

## Related Posts
`jetpack-related-posts` is a list of posts related to the current one. Each one includes the post ID, info about the post, as well as an image. This leads to a resized image at the `i0.wp.com` domain. Removing that as well as all of the query params will get the original image.

## Revisions, Templates, Authors
All of these can only be viewed by admins and those with the proper permissions.

## Links
These all lead to different API endpoints.
- Self: Link to the API for this post
- Collection: link to post API endpoint
- About: Info about the post type
- Author: Endpoint for user info, restricted
- Replies: comments left on the post
- Version History: old versions of this post, restricted
- Predecessor Version: older version of this post, restricted
- wp:featuredmedia: images related to this post, usually hero/banner image
- wp:attachment: media associated with the post. This has a "parent" param, which is the post ID, but the result is only a single image even if the post has more.
- wp:term: links to category and tag endpoints, which can be used to get that info for a given post.
---

# Comments
Comments can be found at `https://estreetshuffle.com/index.php/wp-json/wp/v2/comments`, optionally adding the `?post=[ID]` param to get comments for a specific post. Comments were disabled sitewide when the shutdown was announced.








# Wayback Machine
Since this seems to be the "officially endorsed" method. A rundown of what has been saved.

For this, I will consider the "total post count" to be 2084. This is how many posts I was able to save using the WP API.

WM has the following archived:
- Short Links (https://estreetshuffle.com/?p[ID]): 648
- Long Links: (https://estreetshuffle.com/index.php/...): 9,337
- API (https://estreetshuffle.com/index.php/wp-json/wp/v2/posts/): 1304

Short and long links are the only ones relevant for viewing the sites pages. 