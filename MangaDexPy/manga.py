class Manga:
    """Represents a MangaDex Manga."""
    __slots__ = ("id", "title", "titles", "desc", "locked", "links", "language", "last_volume", "last_chapter",
                 "type", "status", "year", "content", "tags", "created_at", "updated_at", "author", "artist",
                 "chapters", "client")

    def __init__(self, data, rel, client):
        self.id = data["id"]
        self.title = data["attributes"]["title"]
        self.titles = data["attributes"]["altTitles"]
        self.desc = data["attributes"]["description"]
        self.locked = data["attributes"]["isLocked"]
        self.links = data["attributes"]["links"]
        self.language = data["attributes"]["originalLanguage"]
        self.last_volume = data["attributes"]["lastVolume"]
        self.last_chapter = data["attributes"]["lastChapter"]
        self.type = data["attributes"]["publicationDemographic"]
        self.status = data["attributes"]["status"]
        self.year = data["attributes"]["year"]
        self.content = data["attributes"]["contentRating"]
        self.tags = [MangaTag(x) for x in data["attributes"]["tags"]]
        self.created_at = data["attributes"]["createdAt"]
        self.updated_at = data["attributes"]["updatedAt"]
        self.author = [x["id"] for x in rel if x["type"] == "author"]
        self.artist = [x["id"] for x in rel if x["type"] == "artist"]
        self.client = client

    def get_chapters(self):
        return self.client.get_manga_chapters(self)


class MangaTag:
    """Represents a MangaDex Manga Tag."""
    __slots__ = ("id", "name")

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["attributes"]["name"]
