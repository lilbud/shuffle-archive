posts:
    id: uuid pk
    post_id: int
    published: datetime
    last_modified: datetime
    url: str
    title: str
    content: str
    except: str
    author: uuid fk authors
    featured_media: fk media
    updated_at: datetimetz default now()
    created_at: datetimetz default now()

categories:
    id: uuid pk
    category_id: int
    name: str
    updated_at: datetimetz default now()
    created_at: datetimetz default now()

tags:
    id: uuid pk
    tag_id: int
    name: str
    updated_at: datetimetz default now()
    created_at: datetimetz default now()

post_tags:
    post_id: uuid fk posts
    tag_id: uuid fk categories

post_categories:
    post_id: uuid fk posts
    cat_id: uuid fk categories

related_posts
    post_id: uuid fk posts
    related_post: uuid fk posts

authors:
    id: uuid pk
    author_id: int
    name: str
    updated_at: datetimetz default now()
    created_at: datetimetz default now()

media:
    id: uuid pk
    media_id: int
    url: str
    post_id: uuid fk posts
    updated_at: datetimetz default now()
    created_at: datetimetz default now()

comments:
    id: uuid pk
    comment_id: int
    post_id: uuid fk posts
    author_id: uuid fk authors
    text: str
    published: datetime
    updated_at: datetimetz default now()
    created_at: datetimetz default now()