class Group:
    """Represents a MangaDex Group."""
    __slots__ = ("id", "name", "leader", "members", "created_at", "updated_at", "client")

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships")
        self.name = _attrs.get("name")
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        try:
            _members = [x["attributes"] for x in _rel if x["type"] == "member"]
            from .user import User
            self.members = [User(x, client) for x in _rel if x["type"] == "member"]
        except (IndexError, KeyError):
            self.members = [x["id"] for x in _rel if x["type"] == "member"]
        try:
            _leader = [x["attributes"] for x in _rel if x["type"] == "leader"]
            from .user import User
            self.leader = next((User(x, client) for x in _rel if x["type"] == "leader"), None)
        except (IndexError, KeyError):
            self.leader = next((x["id"] for x in _rel if x["type"] == "leader"), None)
        self.client = client
