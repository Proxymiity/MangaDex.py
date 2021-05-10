import time


class NetworkChapter:
    """Represents a link between the MD@H Network and a Chapter."""
    __slots__ = ("valid_thru", "parent_chapter", "node_url", "pages", "pages_redux", "client")

    def __init__(self, chapter, node, client):
        self.valid_thru = int(time.time()) + 900
        self.parent_chapter = chapter
        self.node_url = node
        self.pages = [f"{node}/data/{chapter.hash}/{x}" for x in chapter.pages]
        self.pages_redux = [f"{node}/data-saver/{chapter.hash}/{x}" for x in chapter.pages_redux]
        self.client = client

    def report(self, url, success, cache_header, req_bytes, req_duration):
        return self.client.network_report(url, success, cache_header, req_bytes, req_duration)
