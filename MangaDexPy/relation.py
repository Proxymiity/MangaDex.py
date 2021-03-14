relations = {1: "prequel", 2: "sequel", 3: "adaptation", 4: "spin_off", 5: "side_story", 6: "main", 7: "alternate",
             8: "doujinshi", 9: "based", 10: "colored", 11: "monochrome", 12: "shared_universe", 13: "same_franchise",
             14: "pre_serialization", 15: "serialization"}


class Relation:
    """Represents a MangaDex Manga Relation."""
    __slots__ = ("id", "title", "type", "hentai")

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.type = relations[data["type"]]
        self.hentai = data["isHentai"]
