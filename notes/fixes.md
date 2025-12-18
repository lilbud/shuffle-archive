most of these fixes are handled by html_to_markdown or ftfy

# General Fixes

## replaces extraneous new lines, replaces groups of 2 or more with a single
```
FIND: "(\r?\n){2}"
REPLACE: "<p></p>"
```

# Youtube Fixes

## Replace embedded video with direct link
```
FIND: "youtube.com\/embed\/(?!videoseries)"
REPLACE: "youtube.com/watch?v="
```

## Replace embedded playlist with direct link
```
FIND: "youtube.com\/embed\/videoseries"
REPLACE: "youtube.com/playlist"
```

## Remove embed params
```
FIND: "\?feature=oembed"
REPLACE: ""

FIND: "&feature=oembed"
REPLACE: ""
```

# Videopress Fixes:

## Videopress embed links have a ton of params that are unneeded
```
FIND: "\?hd.*"
REPLACE: ""
```