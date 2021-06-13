from .user import User


class Group:
    """Represents a MangaDex Group."""
    __slots__ = ("id", "name", "leader", "members", "created_at", "updated_at", "client")

    def __init__(self, data, rel, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        self.name = _attrs.get("name")
        self.leader = User(_attrs.get("leader"), [], client)
        self.members = [User(x, [], client) for x in _attrs.get("members")]
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        self.client = rel  # Dummy assignment for the search helper to work properly. Does not affect the object.
        self.client = client
