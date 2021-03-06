class Chapter:
    """Represents a MangaDex Chapter."""
    __slots__ = ("id", "volume", "chapter", "title", "language", "hash", "pages", "pages_redux", "published_at",
                 "created_at", "updated_at", "parent_manga", "group", "uploader", "client")

    def __init__(self, data, rel, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        self.volume = _attrs.get("volume")
        self.chapter = _attrs.get("chapter")
        self.title = _attrs.get("title")
        self.language = _attrs.get("translatedLanguage")
        self.hash = _attrs.get("hash")
        self.pages = _attrs.get("data")
        self.pages_redux = _attrs.get("dataSaver")
        self.published_at = _attrs.get("publishAt")
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        try:
            _manga = [x["attributes"] for x in rel if x["type"] == "manga"]
            from .manga import Manga
            self.parent_manga = next((Manga(x, [], client) for x in rel if x["type"] == "manga"), None)
        except (IndexError, KeyError):
            self.parent_manga = next((x["id"] for x in rel if x["type"] == "manga"), None)
        try:
            _group = [x["attributes"] for x in rel if x["type"] == "scanlation_group"]
            from .group import Group
            self.group = [Group(x, [], client) for x in rel if x["type"] == "scanlation_group"]
        except (IndexError, KeyError):
            self.group = [x["id"] for x in rel if x["type"] == "scanlation_group"]
        try:
            _uploader = [x["attributes"] for x in rel if x["type"] == "user"]
            from .user import User
            self.uploader = next((User(x, [], client) for x in rel if x["type"] == "user"), None)
        except (IndexError, KeyError):
            self.uploader = next((x["id"] for x in rel if x["type"] == "user"), None)
        self.client = client

    def get_md_network(self, force_443: bool = False):
        return self.client.read_chapter(self, force_443)
