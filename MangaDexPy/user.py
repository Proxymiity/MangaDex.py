class User:
    """Represents a MangaDex User."""
    __slots__ = ("id", "username", "client")

    def __init__(self, data, client):
        self.id = data["id"]
        self.username = data["attributes"]["username"]
        self.client = client
