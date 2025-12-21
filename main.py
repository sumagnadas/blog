import os
from os import path
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, PastDatetime
from slugify import slugify

from md_engine import render

app = FastAPI()


class Post(BaseModel):
    title: str
    slug_title: str | None
    publish_date: PastDatetime
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create")
def create_post(post: Post):
    slug_title = post.slug_title
    if not slug_title:
        slug_title = slugify(
            post.title,
            stopwords=[
                "the",
                "a",
                "in",
            ],
            max_length=30,
            word_boundary=True,
            entities=True,
            decimal=True,
            hexadecimal=True,
        )
    if path.exists(f"posts/{slug_title}.md"):
        raise HTTPException(status_code=400, detail="Post already Exists")
    f = open(f"posts/{slug_title}.md", "w")
    f.write(post.content)
    f.close()
    return {"slug_title": slug_title}


@app.post("/edit/{slug_title}")
def edit_post(slug_title: str, post: Annotated[Post, Body()]):
    if path.exists(f"posts/{slug_title}.md"):
        if slug_title != post.slug_title:
            os.remove(f"posts/{slug_title}.md")
        slug_title = post.slug_title
        f = open(f"posts/{slug_title}.md", "w")
        f.write(post.content)
        f.close()
        return {"slug_title": slug_title}
    raise HTTPException(status_code=404, detail="Post not found.")


@app.get("/post/{slug_title}")
def get_post(slug_title: str):
    if path.exists(f"posts/{slug_title}.md"):
        f = open(f"posts/{slug_title}.md")
        content = f.read()
        return {"content": render(content)}
    raise HTTPException(status_code=404, detail="Post not found.")


@app.get("/posts")
def get_posts():
    posts = list(os.walk("posts/"))[0][2]
    posts = [path.splitext(post)[0] for post in posts]
    return {"posts": posts}
