from .partial import PartialChapter, PartialGroup
from .relation import Relation
types = {0: None, 1: "Shounen", 2: "Seinen", 3: "Josei", 4: "Shoujo"}
statuses = {0: None, 1: "ongoing", 2: "completed"}


class Manga:
    """Represents a MangaDex Manga."""
    __slots__ = ("id", "title", "titles", "desc", "artist", "author", "language", "status", "type", "tag_ids",
                 "last_chapter", "last_volume", "hentai", "links", "relations", "ratings", "views", "follows",
                 "comments", "last_upload", "cover", "chapters", "groups", "session")

    def __init__(self, data, session, chaps=None, groups=None):
        self.id = data["id"]
        self.title = data["title"]
        self.titles = data["altTitles"]
        self.desc = data["description"]
        self.artist = data["artist"]
        self.author = data["author"]
        self.language = data["publication"]["language"]
        self.status = statuses[data["publication"]["status"]]
        self.type = types[data["publication"]["demographic"]]
        self.tag_ids = data["tags"]
        self.last_chapter = data["lastChapter"]
        self.last_volume = data["lastVolume"]
        self.hentai = data["isHentai"]
        self.links = data["links"]
        self.relations = [Relation(x) for x in data["relations"] or []]
        self.ratings = data["rating"]
        self.views = data["views"]
        self.follows = data["follows"]
        self.comments = data["comments"]
        self.last_upload = data["lastUploaded"]
        self.cover = data["mainCover"]
        self.chapters = [PartialChapter(x) for x in chaps or []]
        self.groups = [PartialGroup(x) for x in groups or []]
        self.session = session

    def get_tags(self):
        tags = self.session.get("https://api.mangadex.org/v2/tag").json()["data"]
        return [tags[x] for x in tags if int(x) in self.tag_ids]

    def get_covers(self):
        return self.session.get(f"https://api.mangadex.org/v2/manga/{self.id}/covers").json()["data"]
