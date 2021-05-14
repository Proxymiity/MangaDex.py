from .user import User


class Group:
    """Represents a MangaDex Group."""
    __slots__ = ("id", "name", "leader", "members", "created_at", "updated_at", "client")

    def __init__(self, data, client):
        self.id = data["id"]
        self.name = data["attributes"]["name"]
        self.leader = User(data["attributes"]["leader"], client)
        self.members = [User(x, client) for x in data["attributes"]["members"]]
        self.created_at = data["attributes"]["createdAt"]
        self.updated_at = data["attributes"]["updatedAt"]
        self.client = client
