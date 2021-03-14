class PartialChapter:
    """Represents a MangaDex Chapter, but with reduced info."""
    __slots__ = ("id", "hash", "manga_id", "manga_title", "volume", "chapter", "title", "language", "groups",
                 "uploader", "timestamp", "thread_id", "views")

    def __init__(self, data):
        self.id = data["id"]
        self.hash = data["hash"]
        self.manga_id = data["mangaId"]
        self.manga_title = data["mangaTitle"]
        self.volume = data["volume"]
        self.chapter = data["chapter"]
        self.title = data["title"]
        self.language = data["language"]
        self.groups = data["groups"]
        self.uploader = data["uploader"]
        self.timestamp = data["timestamp"]
        self.thread_id = data["threadId"]
        self.views = data["views"]


class PartialGroup:
    """Represents a MangaDex Group, but with reduced info."""
    __slots__ = ("id", "name")

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
