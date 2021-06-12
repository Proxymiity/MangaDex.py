class User:
    """Represents a MangaDex User."""
    __slots__ = ("id", "username", "client")

    def __init__(self, data, rel, client):
        self.id = data["id"]
        self.username = data["attributes"]["username"]
        self.client = rel  # Dummy assignment for the search helper to work properly. Does not affect the object.
        self.client = client
