Things to fix for every post:

# Links:
Any internal links (other ESS pages), remove. Add footnote which indicates where to go, add context for link.

External Links (going offsite) change to archived copy. Add footnote about what the link was and where it pointed

All links get a footnote, explain where link is and what it was. This can act as a "backup", so even if the archived link disappears, the context will not be lost.

# Embedded Videos (Youtube/Videopress/Vimeo?/etc.)
All video links get changed to direct links. Youtube/Videopress were as embeds instead of direct links. I don't foresee this presenting an issue, but to be safe all YT/Videopress links have already been converted to direct links.

Regardless of source, all videos will get a note describing them. At least source/what the video was. Official videos should be fine, but videos on other channels might not be as safe.

# Videopress
Many videos are hosted here, which is Wordpress's hosting site. The files do seem to remain even if the post is deleted. However, I do not know if they'll disappear when the site goes down. Replace these with Youtube/Archive links (if audio only), add note.

# Images
Images can be embedded in ebooks no issue. Add caption if there is none. Change image links to point to local files.

# Audio
Many posts have embedded audio files in a player. If it is a live track, point to RadioNowhere. Redirect to Youtube or Archive whenever possible. All audio has been downloaded locally. For the "archive", redirect links to the local files. For the ebooks, audio CAN be embedded which is nice. Although the better play might just be pointing to YT/Archive. Add note explaining what the audio is.

# Fixes
The `fixes.md` file has a list of all fixes that have been applied to the html already. This list will grow undoubtedly.

# HTML
This will likely need some kind of manual process, checking the HTML in a preview and making sure nothing is broken. Fix things like blockquotes and missing tags.

I do not know if the Standard Ebooks toolset is capable of this or not.

# Organizing Files
Right now, all posts are stored in a folder per post. This contains the original JSON file pulled from the API, the post HTML, and the post converted to Markdown.

# StandardEbooks
Once all fixes are done, and files are mostly clean in terms of formatting. Look into the toolset provided by them, see if it works or not.

---

# Process and Steps
1. Clean and apply fixes to every post HTML to be included. Fix missing tags and links like above.
2. Give files a preview in HTML viewer to ensure they're good
3. Compile all individual files into a single HTML file. Have `h1` elements to indicate "chapters".
4. Run StandardEbook tools. This will generate the epub folder structure for each book. They also have their own tools with fixes
5. Once all is good, generate the books.