most of these fixes are handled by html_to_markdown or ftfy

## replaces extraneous new lines, replaces groups of 2 or more with a single
```
FIND: "(\r?\n){2}"
REPLACE: "<p></p>"
```

# iframe fixes
All iframe elements have been replaced with a direct video link. Markdown does not support iframe elements, so these would need to be replaced anyway.

Additionally, the iframe title has been preserved and made into the link text. Videopress links do not have titles, so these will have to be updated on a per-post basis.

## Empty Lines removed
```
FIND: "^$"
REPLACE: ""
```

## http replaced with https
```
FIND: "http:"
REPLACE: "https:"
```

# Wordpress Image CDN (i0, i1, i2) removed
These links led to a resized version of an image, which can be replaced with a direct link
```
FIND: "i\d.wp.com/"
REPLACE: ""
```

# Wordpress `data` attributes removed
These attributes were to do with Wordpress, and linked to different sized images. All of these can be removed with no impact.

# Extra IMG attrs (srcset, sizes, class, loading, decoding):
More attributes that aren't needed.