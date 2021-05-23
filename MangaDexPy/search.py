from .manga import Manga
from .chapter import Chapter
from .group import Group
from .author import Author
from .cover import Cover
classes = {"manga": Manga, "chapter": Chapter, "group": Group, "author": Author, "cover": Cover}
paths = {"manga": "/manga", "chapter": "/chapter", "group": "/group", "author": "/author", "cover": "/cover"}


class SearchMapping:
    """Gives URLs and Objects based on a string."""
    __slots__ = ("string", "object", "path")

    def __init__(self, obj: str):
        self.string = obj.lower()
        self.object = classes[self.string]
        self.path = paths[self.string]
