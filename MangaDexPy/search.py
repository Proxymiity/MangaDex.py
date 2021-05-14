from .manga import Manga
from .chapter import Chapter
from .group import Group
classes = {"manga": Manga, "chapter": Chapter, "group": Group}
paths = {"manga": "/manga", "chapter": "/chapter", "group": "/group"}


class SearchMapping:
    """Gives URLs and Objects based on a string."""
    __slots__ = ("string", "object", "path")

    def __init__(self, obj: str):
        self.string = obj.lower()
        self.object = classes[self.string]
        self.path = paths[self.string]
