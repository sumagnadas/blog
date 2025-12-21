from markdown_it import MarkdownIt

engine = MarkdownIt(
    "gfm-like",
    {"html": "True", "typographer": "True", "highlight": "True", "linkify": "True"},
)


def render(content: str):
    return engine.render(content)
