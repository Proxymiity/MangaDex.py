class User:
    """Represents a MangaDex User."""
    __slots__ = ("id", "username", "client")

    def __init__(self, data, rel, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        self.username = _attrs.get("username")
        self.client = rel  # Dummy assignment for the search helper to work properly. Does not affect the object.
        self.client = client
