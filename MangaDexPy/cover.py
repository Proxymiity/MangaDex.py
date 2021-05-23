class Cover:
    __slots__ = ("id", "desc", "volume", "file", "parent_manga", "url", "url_512", "url_256", "created_at",
                 "updated_at", "client")

    def __init__(self, data, rel, client):
        self.id = data["id"]
        self.desc = data["attributes"]["description"]
        self.volume = data["attributes"]["volume"]
        self.file = data["attributes"]["fileName"]
        self.parent_manga = next((x["id"] for x in rel if x["type"] == "manga"), None)
        self.url = f"https://uploads.mangadex.org/covers/{self.parent_manga}/{self.file}"
        self.url_512 = f"{self.url}.512.jpg"
        self.url_256 = f"{self.url}.256.jpg"
        self.created_at = data["attributes"]["createdAt"]
        self.updated_at = data["attributes"]["updatedAt"]
        self.client = client
