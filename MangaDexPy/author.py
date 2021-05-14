class Author:
    __slots__ = ("id", "name", "image", "bio", "created_at", "updated_at", "client")

    def __init__(self, data, rel, client):
        self.id = data["id"]
        self.name = data["attributes"]["name"]
        self.image = data["attributes"]["imageUrl"]
        self.bio = data["attributes"]["biography"]
        self.created_at = data["attributes"]["createdAt"]
        self.updated_at = data["attributes"]["updatedAt"]
        self.client = rel  # Dummy assignment for the search helper to work properly. Does not affect the object.
        self.client = client
