class Chapter:
    """Represents a MangaDex Chapter."""
    __slots__ = ("id", "volume", "chapter", "title", "language", "hash", "pages", "pages_redux", "published_at",
                 "created_at", "updated_at", "parent_manga", "group", "uploader", "client")

    def __init__(self, data, rel, client):
        self.id = data["id"]
        self.volume = data["attributes"]["volume"]
        self.chapter = data["attributes"]["chapter"]
        self.title = data["attributes"]["title"]
        self.language = data["attributes"]["translatedLanguage"]
        self.hash = data["attributes"]["hash"]
        self.pages = data["attributes"]["data"]
        self.pages_redux = data["attributes"]["dataSaver"]
        self.published_at = data["attributes"]["publishAt"]
        self.created_at = data["attributes"]["createdAt"]
        self.updated_at = data["attributes"]["updatedAt"]
        self.parent_manga = next((x["id"] for x in rel if x["type"] == "manga"), None)
        self.group = [x["id"] for x in rel if x["type"] == "scanlation_group"]
        self.uploader = next((x["id"] for x in rel if x["type"] == "user"), None)
        self.client = client

    def get_md_network(self, force_443: bool = False):
        return self.client.read_chapter(self, force_443)
