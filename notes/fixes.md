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

---

Below is a list of specific post fixes, primarily fixing formatting quirks and issues with links and what not.:

2018-03-03-it-s-a-crossover-my-first-podcast-experience:

```
Original: S*[et Lusting Bruce](https://setlustingbruce.libsyn.com/)*
Fixed: *[Set Lusting Bruce](https://setlustingbruce.libsyn.com/)*
```

2025-11-28-thirty-seven-days-out

```
Original: The Internet Archive's[Wayback Machine](https://web.archive.org/) will likely preserve previous versions of the site for a long time to come.

Fixed: The Internet Archive's [Wayback Machine](https://web.archive.org/) will likely preserve previous versions of the site for a long time to come.
```

```
Original: I've heard good things about both [Blogbooker](https://blogbooker.com/) and[printmy.blog](https://printmy.blog/),

Fixed: I've heard good things about both [Blogbooker](https://blogbooker.com/) and [printmy.blog](https://printmy.blog/),
```

2025-01-01-introduction

title changed to "Kingdom of Days Volume 1 Introduction", excerpt changed to "_Kingdom of Days_ was never supposed to be a book, let alone a twelve-volume series.". This was one of the "mangled" posts, and was actually a reused version of the Year Two post.

---

2011-01-01-introduction (id 390, post: 28453)

title changed to "Roll of the Dice Volume 1 Introduction". Excerpt changed to ""Why don't you start a blog?" my wife asked.". Post is the introduction to the first Roll of the Dice Book.

Original post was "Blogger’s Note: Video omissions in daily e-mails". Unarchived and missing.

Added second entry with original title/excerpt and post/published date.

---
2011-01-31-visitation-at-fort-horn (id: 419, post: 7109)

Excerpt changed to "The only *Greetings* outtake I never got around to writing about".

Originally "Blogger’s Note: Kingdom of Days". Unarchived and missing.

Added second entry with original title/excerpt and post/published date.

---

2019-04-11-blogger-s-note-important-update (id: 2, post: 8825)

Title -> "Cover Me Book Introduction"
Excerpt -> "Shhh.... I'll let you in on a secret, but you can't tell anyone. *Cover Me* is my favorite."

Post was originally "Blogger’s Note: Important Update", having to do with missing video links.

Added second entry with original title/excerpt and post/published date.

---

these posts had their titles changed from "introduction" to the below.
43: Cover Me: One Time Only Introduction
4575: ROTD: Born In The U.S.A. Introduction
4521: ROTD: Lucky Town Introduction
4605: ROTD: Lucky Town Introduction
340: ROTD: Lucky Town Introduction
368: ROTD: We Shall Overcome Introduction
425: ROTD: Letter To You Introduction

---

40635 Follow That Dream (ID: 47, 4155)

Old Excerpt: "A note of thanks for your readership this past year and a look ahead to the next one!"

New Excerpt: "A ghost story, and a cautionary tale. But it started out as a musical comedy."
