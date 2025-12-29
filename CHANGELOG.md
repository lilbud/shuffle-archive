# 2025-12-11
- Initial commit.
- Add all posts grabbed from 11-30 to 12-11.

# 2025-12-13
- Update parsing function with list of manual Regex fixes. These are things that the html parser wouldn't catch. See `fixes.txt`
- Posts are now saved as HTML rather than converted markdown

# 2025-12-18
- Move any notes to their own folder
- Add `report.txt` to log number of posts/pages found each day
- Start including database backup

# 2025-12-20
- Add KoD 12/19 and 12/20

# 2025-12-22
- Add KoD 12/21 and 12/22

# 2025-12-23
- Add KoD 12/23

# 2025-12-24
- Add KoD 12/24
- Add several posts which were "replaced in place" but kept same ID

# 2025-12-28
- Add KoD 12/25-28

# 2025-12-29
- Add KoD 12/29
- Add latest database backup
- Add function to get recently updated posts. I found that many posts are being "updated", having their content entirely replaced but keeping the same ID.
- JSON file naming update. Files are now named like so `ID_MODIFIED-TIMESTAMP.json`. Posts are saved with their `modified` timestamp appended. Goes hand-in-hand with the above, saving newer versions of posts.