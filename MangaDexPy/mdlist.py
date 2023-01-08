class MDList:
    """Represents a user created MDList"""
    __slots__ = ("id", "name", "visibility", "titles", "creator","client")

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships", [])
        self.name = _attrs.get("name")
        self.visibility = _attrs.get("visibility")
        self.titles = [x["id"] for x in _rel if x["type"] == "manga"]
        self.creator = next((x["id"] for x in _rel if x["type"] == "user"), None)
        self.client = client