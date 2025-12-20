from os import path
from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PastDatetime
from slugify import slugify

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


@app.post("/edit")
def edit_post(post: Post):
    return {"slug_title": post.slug_title}


@app.get("/post/{slug_title}")
def get_post(slug_title: str):
    if path.exists(f"posts/{slug_title}.md"):
        f = open(f"posts/{slug_title}.md")
        content = f.read()
        return {"content": content}
    raise HTTPException(status_code=404, detail="Post not found.")
